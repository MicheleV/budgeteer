# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import calendar
import datetime
from dateutil.relativedelta import relativedelta
import math
import os

from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.db.models import F
from django.db.models import Case
from django.db.models import When
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from graphs import plot
from rest_framework.decorators import api_view
from rest_framework.response import Response

import budgets.forms as f
import budgets.models as m
from budgets.serializers import CategorySerializer
import budgets.views_utils as utils


###############################################################################
# Class based views
###############################################################################

# TODO: find out how to decorate Classes as_view() function
# https://jsatt.com/blog/decorators-vs-mixins-for-django-class-based-views
# @require_http_methods(["GET"])
# def dispatch(self, request, *args, **kwargs):
#     return super(CategoryListView, self).dispatch(request, *args, **kwargs)

class CategoryCreateView(CreateView):
    model = m.Category
    form_class = f.CategoryForm

    def get_success_url(self):
        return reverse('categories')


class CategoryListView(ListView):
    model = m.Category


class ExpenseCreateView(CreateView):
    model = m.Expense
    form_class = f.ExpenseForm

    def get_success_url(self):
        return reverse('expenses_create')
# TODO change tests to account for this new redirect

# class ProfileContextMixin(generic_base.ContextMixin, generic_view.View):
#     @cached_property
#     def profile(self):
#         return get_object_or_404(Profile, user__username=self.request.user)

#     def get_context_data(self, **kwargs):
#         context = super(ProfileContextMixin, self).get_context_data(**kwargs)
#         context['profile'] = self.profile
#         return context


# FIXME: Aggregate manually as Django ORM is issuing LOTS of duplicated queries
# class ExpenseListView(ProfileContextMixin):
class ExpenseListView(ListView):
    model = m.Expense

    # Try this instead https://stackoverflow.com/a/37959458/2535658
    @cached_property
    def profile(self):
        pass
        # expenses = m.Expense.objects.filter(date__range=(start, end)) \
        # .order_by('-date', '-id')
        # Do this manually to avoid double queries
        # expenses_sum = expenses.aggregate(Sum('amount'))['amount__sum']
        # return get_object_or_404(Profile, user__username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start = yymm_date = self.kwargs.get('start', None)
        end = yymm_date = self.kwargs.get('end', None)

        # TODO: Look into how to share data with get_queryset()
        # context['xxxx'] = self.get_queryset()
        # Try this instead https://stackoverflow.com/a/37959458/2535658
        # context['expenses, adding garbage to prevent overwrite']=self.profile

        # Toggle delete buttons
        show_delete = self.request.GET.get('delete', False) == '1'
        context['show_delete'] = show_delete

        # TODO: this code is exactly the same as get_queryset(),memoized it
        if end is None:
            (start, end) = utils.get_month_boundaries(start)
        else:
            format_str = '%Y-%m-%d'
            start = datetime.datetime.strptime(start, format_str).date()

        # TODO: this code is exactly the same as get_queryset(), memoized it!
        # TODO refactor these queries after reading Django annotation docs
        # and aggregation
        expenses = m.Expense.objects.filter(date__range=(start, end)) \
                    .order_by('-date', '-id')
        expenses_sum = expenses.aggregate(Sum('amount'))['amount__sum']
        pie_graph = utils.generate_current_month_expenses_pie_graph(expenses)
        context['pie_graph'] = pie_graph
        context['expenses_sum'] = expenses_sum
        return context

    def get_queryset(self):
        start = yymm_date = self.kwargs.get('start', None)
        end = yymm_date = self.kwargs.get('end', None)

        # TODO: this code is exactly the same as get_context_data(),memoized it
        if end is None:
            (start, end) = utils.get_month_boundaries(start)
        else:
            format_str = '%Y-%m-%d'
            start = datetime.datetime.strptime(start, format_str).date()
        # TODO: refactor these queries after reading Django annotation docs
        # and aggregation
        expenses = m.Expense.objects.filter(date__range=(start, end)) \
                    .order_by('-date', '-id')
        expenses_sum = expenses.aggregate(Sum('amount'))['amount__sum']

        return expenses


class ExpenseDeleteView(DeleteView):
    model = m.Expense

    def get_success_url(self):
        return reverse('expenses')


class MonthlyBudgetsCreateView(CreateView):
    model = m.MonthlyBudget
    form_class = f.MonthlyBudgetForm

    def get_success_url(self):
        return reverse('monthly_budgets')


class MonthlyBudgetListView(ListView):
    model = m.MonthlyBudget

    def get_queryset(self):
        yymm_date = self.kwargs.get('date', None)
        if yymm_date is None:
            mb = m.MonthlyBudget.objects. \
                              select_related('category').all()
        else:
            full_date = f"{yymm_date}-01"
            mb = m.MonthlyBudget.objects.select_related('category'). \
                filter(date=full_date)
        return mb


class MonthlyBudgetDetailView(DetailView):
    model = m.MonthlyBudget


class GoalCreateView(CreateView):
    model = m.Goal
    form_class = f.GoalForm


class GoalListView(ListView):
    model = m.Goal


class GoalDetailView(DetailView):
    model = m.Goal


class IncomeCategoryCreateView(CreateView):
    model = m.IncomeCategory
    form_class = f.IncomeCategoryForm

    def get_success_url(self):
        return reverse('income_categories')


class IncomeCategoryView(ListView):
    model = m.IncomeCategory


class IncomeCategoryDetailView(DetailView):
    model = m.IncomeCategory


class IncomCreateView(CreateView):
    model = m.Income
    form_class = f.IncomeForm

    def get_success_url(self):
        return reverse('incomes')


class IncomeView(ListView):
    model = m.Income

    def get_queryset(self):
        start = yymm_date = self.kwargs.get('start', None)
        end = yymm_date = self.kwargs.get('end', None)

        # TODO: use the date parameter if present to filter
        #       (add url to grab start and end)
        if end is None:
            (start, end) = utils.get_month_boundaries(start)
        else:
            format_str = '%Y-%m-%d'
            start = datetime.datetime.strptime(start, format_str).date()
        incomes = m.Income.objects.filter(date__range=(start, end))
        return incomes


class MonthlyBalanceCategoryCreateView(CreateView):
    model = m.MonthlyBalanceCategory
    form_class = f.MonthlyBalanceCategoryForm

    def get_success_url(self):
        return reverse('monthly_balance_categories')


class MonthlyBalanceCategoryView(ListView):
    model = m.MonthlyBalanceCategory


class MonthlyBalanceCategoryDetailView(DetailView):
    model = m.MonthlyBalanceCategory


class MonthlyBalancesCreateView(CreateView):
    model = m.MonthlyBalance
    form_class = f.MonthlyBalanceForm

    def get_success_url(self):
        return reverse('monthly_balances')


class MonthlyBalancesView(ListView):
    # TODO: find out if we can avoid using a model inside ListView
    # inside get_context_data(), we're re-issuing the same query!
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
            )))

        # Display only not archived goals
        goals = m.Goal.objects.filter(is_archived=False)
        if len(mb) > 0:
            bar_graph = utils.generate_monthly_balance_bar_graph(mb, goals)

        total = mb.aggregate(Sum('amount'))['amount__sum']
        context['monthly_balances'] = mb
        context['bar_graph'] = bar_graph
        context['total'] = total
        context['show_delete'] = show_delete
        return context


# Show monhtly balances for a given month
class MonthlyBalancesSingleMonthView(ListView):
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

        mb = m.MonthlyBalance.objects.select_related('category'). \
            filter(date=complete_date).order_by('date')

        # NOTE: not using Django's ORM annotate to avoid issuing a second query
        total = 0
        for a in mb:
            if a.category.is_foreign_currency:
                a.real_amount = a.amount * rate
            else:
                a.real_amount = a.amount
            total += a.real_amount

        context['monthly_balances'] = mb
        context['total'] = total
        context['show_delete'] = show_delete
        context['currency'] = currency
        return context


# This class is reusing the same template as MonthlyBalancesCreateView
class MonthlyBalanceUpdateView(UpdateView):
    model = m.MonthlyBalance
    form_class = f.MonthlyBalanceForm

    def get_success_url(self):
        return reverse('monthly_balances')


class MonthlyBalanceDeleteView(DeleteView):
    model = m.MonthlyBalance

    def get_success_url(self):
        return reverse('monthly_balances')

###############################################################################
# API
###############################################################################

# TODO: move me inside a namespace
@api_view(['GET'])
# @renderer_classes([JSONRenderer])
def api_categories(request):
    """
    List all categories
    """
    categories = m.Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

###############################################################################
# Function based classes
###############################################################################


@require_http_methods(["GET", "POST"])
def multiple_new_mohtly_balance(request):
    categories = m.MonthlyBalanceCategory.objects.filter()
    cats = categories.count()
    MBFormSet = formset_factory(form=f.MonthlyBalanceForm, extra=cats,
                                max_num=cats)

    if request.method == 'POST':
        formset = MBFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
            return redirect('monthly_balances')
    else:
        intial_data = []
        date = utils.get_month_boundaries()[1]
        print(utils.get_month_boundaries())
        for c in categories:
            intial_data.append({'date': '2020-06-01', 'category': c.id})
        formset = MBFormSet(initial=intial_data)

    return render(request, 'budgets/multiple_monthly_budget_form.html',
                  {'formset': formset})


# TODO: write me
@require_http_methods(["GET", "POST"])
def edit_new_monthly_balance(request):
    pass


@require_http_methods(["GET"])
def home_page(request):
    """
    Display the home page
    """
    currency = os.getenv("CURRENCY")
    rate = int(os.getenv("EXCHANGE_RATE"))
    (start, end) = utils.current_month_boundaries()

    # Get current and preivous month balances
    current_balance = utils.get_total_of_monthly_balances(start)
    prev_month = utils.get_previous_month_first_day_date(start)
    starting_balance = utils.get_total_of_monthly_balances(prev_month)

    # Fetch previous month data to compare it with the current month's
    prev_mb, prev_tot = utils.get_month_balance_stats(prev_month, rate)
    current_mb, curr_tot = utils.get_month_balance_stats(start, rate)

    # Display pie graph
    pie_graph = utils.generate_current_monthly_balance_pie_graph(current_mb)

    # TODO: use 1 year or 6 months, instead of 2 months
    curr_tot, diff, diff_perc = utils.calc_increase_perc(curr_tot, prev_tot)

    # Display bar graph (only draw "active" goals)
    goals = utils.get_goals_and_time_to_completions(curr_tot, diff)
    mb = m.MonthlyBalance.objects.select_related('category').values('date'). \
        annotate(actual_amount=Sum(Case(
          When(category__is_foreign_currency=False, then='amount'),
          When(category__is_foreign_currency=True, then=F('amount') * rate)
        ))).order_by('date')

    bar_graph = utils.generate_monthly_balance_bar_graph(mb, goals)

    return render(request, 'home.html', {
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
