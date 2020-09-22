# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import datetime
import os

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models import F
from django.db.models import Case
from django.db.models import When
from django.core.exceptions import PermissionDenied
from django.forms import formset_factory
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

import budgets.forms as f
import budgets.models as m
import budgets.views_utils as utils


###############################################################################
# Class based views
###############################################################################

@method_decorator(login_required, name='dispatch')
class CategoryCreateView(CreateView):
    """Create Expense Category View"""
    model = m.Category
    form_class = f.CategoryForm
    error_msg = 'Category with this Text already exists'
    url = 'budgets:categories'

    def form_valid(self, form):
        return utils.check_constraints_workaround(self, form,
                                                  CategoryCreateView.error_msg,
                                                  CategoryCreateView.url)

    def get_success_url(self):
        """Redirect on create success"""
        return reverse('budgets:categories')


@method_decorator(login_required, name='dispatch')
class CategoryListView(ListView):  # pylint: disable=R0903; # noqa
    model = m.Category
    paginate_by = 15
    ordering = ['id']

    def get_queryset(self):
        return m.Category.objects.filter(
                 created_by=self.request.user).order_by('id')


@method_decorator(login_required, name='dispatch')
class ExpenseCreateView(CreateView):
    model = m.Expense
    form_class = f.ExpenseForm

    def get_form_kwargs(self):
        """Inject user object in the form"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect on create success"""
        return reverse('budgets:expenses_create')


@method_decorator(login_required, name='dispatch')
class ExpenseListView(ListView):
    model = m.Expense
    paginate_by = 30
    ordering = ['id']

    def start_end(self):
        start = self.kwargs.get('start', None)
        end = self.kwargs.get('end', None)
        if end is None:
            (start, end) = utils.get_month_boundaries(start)
        else:
            format_str = '%Y-%m-%d'
            start = datetime.datetime.strptime(start, format_str).date()
        return (start, end)

    @cached_property
    def profile(self):
        start, end = self.start_end()
        expenses = m.Expense.objects.select_related('category').filter(
                   date__range=(start, end),
                   created_by=self.request.user).order_by('-date', '-id')
        return expenses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start, end = self.start_end()

        # Toggle delete buttons
        show_delete = self.request.GET.get('delete', False) == '1'
        context['show_delete'] = show_delete

        expenses = self.profile
        expenses_sum = 0
        for _ in expenses:
            expenses_sum += _.amount
        context['expenses_sum'] = expenses_sum

        # Get monthly budgets only for categoris having expenses in that month
        exp_aggregates = utils.aggregate_expenses_by_category(expenses)

        monthly_budgets = m.MonthlyBudget.objects.select_related(
                          'category').filter(date=start, created_by=self.request.user)

        # FIX ME: do not show budgets if both start and end are not None
        # Just show the sum!

        # TODO: show the sum even for non-budgeted categories

        # Add budgeted amount to expenses aggregates
        for _ in monthly_budgets:
            if _.category.text in exp_aggregates:
                total = exp_aggregates[_.category.text]
                exp_aggregates[_.category.text] = {'total': total,
                                                   'budgeted': _.amount}
            else:
                total = _.amount
                exp_aggregates[_.category.text] = {'total': 0,
                                                   'budgeted': _.amount}
        context['exp_aggregates'] = exp_aggregates

        # TODO: add a new route that autofills budgets based on get param
        # e.g. /monthly_budgets/create?cat_id=32&date=2020-06

        pie_graph = utils.generate_current_month_expenses_pie_graph(expenses)
        context['pie_graph'] = pie_graph
        return context

    def get_queryset(self):
        expenses = self.profile
        return expenses


@method_decorator(login_required, name='dispatch')
class ExpenseDeleteView(DeleteView):  # pylint: disable=R0903; # noqa
    model = m.Expense

    # FIX ME: check for permissions here
    def get_success_url(self):  # pylint: disable=R0201; # noqa
        """Redirect on delete success"""
        return reverse('budgets:expenses')


@method_decorator(login_required, name='dispatch')
class MonthlyBudgetsCreateView(CreateView):
    model = m.MonthlyBudget
    form_class = f.MonthlyBudgetForm

    def get_initial(self):
        initial = super().get_initial()

        initial['date'] = self.request.GET.get('date', None)
        return initial

    def get_form_kwargs(self):
        """Inject user object in the form"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):  # pylint: disable=R0201; # noqa
        """Redirect on create success"""
        return reverse('budgets:monthly_budgets')


@method_decorator(login_required, name='dispatch')
class MonthlyBudgetListView(ListView):  # pylint: disable=R0903; # noqa
    model = m.MonthlyBudget
    paginate_by = 15
    ordering = ['id']

    def get_queryset(self):
        yymm_date = self.kwargs.get('date', None)
        if yymm_date is None:
            mb = m.MonthlyBudget.objects.filter(
                 created_by=self.request.user).select_related(
                 'category').all().order_by('-date')
        else:
            full_date = f"{yymm_date}-01"
            mb = m.MonthlyBudget.objects.filter(
                 date=full_date, created_by=self.request.user).select_related(
                 'category').order_by('-date')
        return mb


@method_decorator(login_required, name='dispatch')
class MonthlyBudgetDetailView(DetailView):
    model = m.MonthlyBudget
    # FIX ME: check for permissions


@method_decorator(login_required, name='dispatch')
class GoalCreateView(CreateView):
    model = m.Goal
    form_class = f.GoalForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):  # pylint: disable=R0201; # noqa
        """Redirect on create success"""
        return reverse('budgets:goals')


@method_decorator(login_required, name='dispatch')
class GoalListView(ListView):  # pylint: disable=R0903; # noqa
    model = m.Goal
    paginate_by = 15
    ordering = ['id']

    def get_queryset(self):
        return m.Goal.objects.filter(
                 created_by=self.request.user).order_by('id')


@method_decorator(login_required, name='dispatch')
class GoalDetailView(DetailView):
    model = m.Goal
    # FIX ME: check permissions here


@method_decorator(login_required, name='dispatch')
class IncomeCategoryCreateView(CreateView):
    model = m.IncomeCategory
    form_class = f.IncomeCategoryForm
    error_msg = 'Income category with this Text already exists'
    url = 'budgets:income_categories'

    def form_valid(self, form):
        return utils.check_constraints_workaround(self, form,
                                                  IncomeCategoryCreateView.error_msg,
                                                  IncomeCategoryCreateView.url)

    def get_success_url(self):  # pylint: disable=R0201; # noqa
        """Redirect on create success"""
        return reverse('budgets:income_categories')


@method_decorator(login_required, name='dispatch')
class IncomeCategoryView(ListView):  # pylint: disable=R0903; # noqa
    model = m.IncomeCategory
    paginate_by = 15
    ordering = ['id']

    def get_queryset(self):
        return m.IncomeCategory.objects.filter(
                 created_by=self.request.user).order_by('id')


@method_decorator(login_required, name='dispatch')
class IncomeCategoryDetailView(DetailView):
    model = m.IncomeCategory
    # FIX ME: check permissions here


@method_decorator(login_required, name='dispatch')
class IncomCreateView(CreateView):
    model = m.Income
    form_class = f.IncomeForm

    def get_form_kwargs(self):
        """Inject user object in the form"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):  # pylint: disable=R0201; # noqa
        """Redirect on create success"""
        return reverse('budgets:incomes')


@method_decorator(login_required, name='dispatch')
class IncomeView(ListView):  # pylint: disable=R0903; # noqa
    model = m.Income
    paginate_by = 15
    ordering = ['id']
    template_name = 'budgets/income_list.html'

    def get_queryset(self):
        start = self.kwargs.get('start', None)
        end = self.kwargs.get('end', None)

        # TODO: add a route to filter by start and end
        if end is None:
            (start, end)           = utils.get_month_boundaries(start)
        else:
            format_str = '%Y-%m-%d'
            start = datetime.datetime.strptime(start, format_str).date()

        incomes = m.Income.objects.filter(
                  date__range=(start, end),
                  created_by=self.request.user).order_by('id')
        return incomes


@method_decorator(login_required, name='dispatch')
class MonthlyBalanceCategoryCreateView(CreateView):
    model = m.MonthlyBalanceCategory
    form_class = f.MonthlyBalanceCategoryForm
    error_msg = 'MonthlyBalanceCategory with this Text already exists'
    url = 'budgets:monthly_balance_categories'

    # Issue: Unique together contraints are not checked, and it look like this
    # is not going to be working in Django **2.2** anytime soon [1]
    def form_valid(self, form):
        return utils.check_constraints_workaround(self, form,
                                                  MonthlyBalanceCategoryCreateView.error_msg,
                                                  MonthlyBalanceCategoryCreateView.url)

    def get_success_url(self):  # pylint: disable=R0201; # noqa
        """Redirect on create success"""
        return reverse('budgets:monthly_balance_categories')


@method_decorator(login_required, name='dispatch')
class MonthlyBalanceCategoryView(ListView):  # pylint: disable=R0903; # noqa
    model = m.MonthlyBalanceCategory
    paginate_by = 15
    ordering = ['id']

    def get_queryset(self):  # pylint: disable=R0201; # noqa
        return m.MonthlyBalanceCategory.objects.filter(
                 created_by=self.request.user).order_by('id')


@method_decorator(login_required, name='dispatch')
class MonthlyBalanceCategoryDetailView(DetailView):  # pylint: disable=R0903; # noqa
    model = m.MonthlyBalanceCategory
    # FIX ME: check permissions here


@method_decorator(login_required, name='dispatch')
class MonthlyBalancesCreateView(CreateView):
    model = m.MonthlyBalance
    form_class = f.MonthlyBalanceForm

    def get_form_kwargs(self):
        """Inject user object in the form"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):  # pylint: disable=R0201; # noqa
        """Redirect on create success"""
        return reverse('budgets:monthly_balances')


@method_decorator(login_required, name='dispatch')
class MonthlyBalancesView(ListView):  # pylint: disable=R0903; # noqa
    model = m.MonthlyBalance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Toggle delete buttons
        show_delete = self.request.GET.get('delete', False) == '1'

        rate = int(os.getenv("EXCHANGE_RATE"))
        total = None
        bar_graph = False

        mb = m.MonthlyBalance.objects.select_related('category'). \
            values('date').order_by('date'). \
            annotate(amount=Sum(Case(
              When(category__is_foreign_currency=False, then='amount'),
              When(category__is_foreign_currency=True, then=F('amount') * rate)
            ))).filter(created_by=self.request.user)
        total = 0
        for _ in mb:
            total += _['amount']

        # Display only not archived goals
        goals = m.Goal.objects.filter(
                is_archived=False, created_by=self.request.user)
        if len(mb) > 0:
            bar_graph = utils.generate_monthly_balance_bar_graph(mb, goals)

        context['monthly_balances'] = mb
        context['bar_graph'] = bar_graph
        context['total'] = total
        context['show_delete'] = show_delete
        return context


@method_decorator(login_required, name='dispatch')
class MonthlyBalancesSingleMonthView(ListView):  # pylint: disable=R0903; # noqa
    """
    Show monhtly balances for a given month
    """
    model = m.MonthlyBalance

    template_name = 'budgets/monthlybalance_singlemonth_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Toggle delete buttons
        show_delete = self.request.GET.get('delete', False) == '1'
        date = self.kwargs.get('date', None)
        complete_date = f"{date}-01"
        rate = int(os.getenv("EXCHANGE_RATE"))
        currency = os.getenv("CURRENCY")

        mb = m.MonthlyBalance.objects.select_related('category').filter(
             date=complete_date, created_by=self.request.user).order_by('date')

        total = 0
        for _ in mb:
            if _.category.is_foreign_currency:
                _.real_amount = _.amount * rate
            else:
                _.real_amount = _.amount
            total += _.real_amount

        context['monthly_balances'] = mb
        context['total'] = total
        context['show_delete'] = show_delete
        context['currency'] = currency
        return context


# This class is reusing the same template as MonthlyBalancesCreateView
@method_decorator(login_required, name='dispatch')
class MonthlyBalanceUpdateView(UpdateView):
    model = m.MonthlyBalance
    form_class = f.MonthlyBalanceForm

    def get_form_kwargs(self):
        """Inject user object in the form"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, *args, **kwargs):
        """Check object ownership"""
        obj = super().get_object(*args, **kwargs)
        if obj.created_by != self.request.user:
            # TODO: create a proper 403 page
            raise PermissionDenied()
        return obj

    def get_success_url(self):
        """Redirect on update success"""
        return reverse('budgets:monthly_balances')


@method_decorator(login_required, name='dispatch')
class MonthlyBalanceDeleteView(DeleteView):
    model = m.MonthlyBalance

    # FIX ME: check permissions here
    def get_success_url(self):
        """Redirect on delete success"""
        return reverse('budgets:monthly_balances')


###############################################################################
# Function based classes
###############################################################################
@login_required
@require_http_methods(["GET", "POST"])
def multiple_new_monthly_budget(request):
    categories = m.Category.objects.filter(is_archived=False, created_by=request.user)
    cats = categories.count()
    MBFormSet = formset_factory(form=f.MonthlyBudgetForm, extra=cats,
                                max_num=cats)

    curr_month_start = utils.get_month_boundaries()[0]
    prev_month_start = utils.get_previous_month_first_day_date(
                       curr_month_start)
    if request.method == 'POST':
        formset = MBFormSet(data=request.POST, form_kwargs={'user': request.user})
        # FIXME: we are not handling when the user submit forms with the same
        # category, and we're also not handling creation of monthly_budgets
        # that already exists for that (category - date combination)
        if formset.is_valid():
            for form in formset:
                form.instance.created_by = request.user
                form.save()
            return redirect('budgets:monthly_budgets')
    else:
        # Prepopulate the form date field, and select a different category
        # for each form
        intial_data = []
        for c in categories:
            intial_data.append({'date': curr_month_start, 'category': c.id})
        formset = MBFormSet(initial=intial_data, form_kwargs={'user': request.user})

    prev_month_monthly_budgets = m.MonthlyBudget.objects.filter(
                                 date=prev_month_start)
    prev_month_dic = {}
    for _ in prev_month_monthly_budgets:
        prev_month_dic[int(_.category.id)] = _.amount

    return render(request, 'budgets/multiple_monthly_budget_form.html',
                  {'formset': formset,
                   'previous_budgets': prev_month_dic})


@login_required
@require_http_methods(["GET", "POST"])
def multiple_new_monthly_balance(request):
    categories = m.MonthlyBalanceCategory.objects.filter(created_by=request.user)
    cats = categories.count()
    MbFormSet = formset_factory(form=f.MonthlyBalanceForm, extra=cats,
                                max_num=cats)

    curr_month_start = utils.get_month_boundaries()[0]
    prev_month_start = utils.get_previous_month_first_day_date(curr_month_start)
    if request.method == 'POST':
        formset = MbFormSet(data=request.POST, form_kwargs={'user': request.user})
        # FIXME: we are not handling when the user submit forms with the same
        # category, and we're also not handling creation of monthly_balance
        # that already exists for that (category - date combination)
        if formset.is_valid():
            for form in formset:
                form.instance.created_by = request.user
                form.save()
            return redirect('budgets:monthly_balances')
    else:
        intial_data = []
        for c in categories:
            intial_data.append({'date': curr_month_start, 'category': c.id})
        formset = MbFormSet(initial=intial_data, form_kwargs={'user': request.user})

    prev_month_monthly_balances = m.MonthlyBalance.objects.filter(
                                  date=prev_month_start, created_by=request.user)
    prev_month_dic = {}
    for _ in prev_month_monthly_balances:
        prev_month_dic[int(_.category.id)] = _.amount

    return render(request, 'budgets/multiple_monthly_balance_form.html',
                  {'formset': formset,
                   'previous_budgets': prev_month_dic})


# TODO: write me
@login_required
@require_http_methods(["GET", "POST"])
def edit_new_monthly_balance(request):
    pass
    # FIX ME: check permissions here


@require_http_methods(["GET"])
def landing_page(request):
    return render(request, 'landing_page.html')


@login_required
@require_http_methods(["GET"])
def home_page(request):
    """Display the home page"""
    currency = os.getenv("CURRENCY")
    # TODO: refactor this to enable multiple currencies (and enable currency
    # rates to be edited inside the app: drop the value from .env file)
    rate = int(os.getenv("EXCHANGE_RATE"))
    (start, end) = utils.current_month_boundaries()
    user = request.user

    # Get current and preivous month balances
    current_balance = utils.get_total_of_monthly_balances(start, user)
    prev_month = utils.get_previous_month_first_day_date(start)
    starting_balance = utils.get_total_of_monthly_balances(prev_month, user)

    # Fetch previous month data to compare it with the current month's
    prev_mb, prev_tot = utils.get_month_balance_stats(prev_month, rate, user)
    current_mb, curr_tot = utils.get_month_balance_stats(start, rate, user)

    # Display pie graph
    pie_graph = utils.generate_current_monthly_balance_pie_graph(current_mb)

    # TODO: use 1 year or 6 months, instead of 2 months
    curr_tot, diff, diff_perc = utils.calc_increase_perc(curr_tot, prev_tot)

    # Display bar graph: only draw active goals
    goals = utils.get_goals_and_time_to_completions(curr_tot, diff)
    # FIXME: filter by current user
    mb = m.MonthlyBalance.objects.select_related('category').values('date'). \
        annotate(actual_amount=Sum(Case(
          When(category__is_foreign_currency=False, then='amount'),
          When(category__is_foreign_currency=True, then=F('amount') * rate)
        ))).order_by('date')

    bar_graph = utils.generate_monthly_balance_bar_graph(mb, goals)

    return render(request, 'home.html',  {
        'current_balance': current_balance,
        'starting_balance': starting_balance,
        # TODO: do this on the template side
        'currency': currency,
        'bar_graph': bar_graph,
        'pie_graph': pie_graph,
        'current_mb': current_mb,
        'current_mb_total': curr_tot,
        'prev_mb': prev_mb,
        'prev_mb_total': prev_tot,
        'two_months_diff': diff,
        'two_months_diff_perc': diff_perc,
        'goals': goals,
    })

