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
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import DetailView
from dotenv import load_dotenv
from graphs import plot
from rest_framework.decorators import api_view
from rest_framework.response import Response

import budgets.forms as f
import budgets.models as m
from budgets.serializers import CategorySerializer

# TODO: is this really needed? Check whether to do load_dotenv() inside urls.py
# once is enough or not
load_dotenv()


# TODO: move these methods to an utility class
def get_previous_month_first_day_date(date):
    """
    Return the first day of the previous month
    """
    return (date - relativedelta(months=1)).replace(day=1)


def get_total_of_monthly_balances(date):
    """
    Return the sum of the monthly balances for the input date
    """
    rate = os.getenv("EXCHANGE_RATE")
    balances = m.MonthlyBalance.objects.select_related('category').filter(date=date)
    return balances.aggregate(correct_sum=Sum(Case(
      When(category__is_foreign_currency=False, then='amount'),
      When(category__is_foreign_currency=True, then=F('amount') * rate)
    )))['correct_sum']


def get_month_boundaries(date):
    """
    Return a tuple composed of the first and the last day
    of month passed as parameter, as datetime objects

    Note: set timezone when providing! Otherwise efault timezone will be UTC
    If th server is actually in a different time zone, beware off-by-one
    month errors when using this function
    """
    if not date:
        start = datetime.date.today().replace(day=1)
    else:
        complete_date = f"{date}-01"
        format_str = '%Y-%m-%d'
        start = datetime.datetime.strptime(complete_date, format_str).date()

    month_range = calendar.monthrange(start.year, start.month)
    last_day_of_month = month_range[1]
    end = datetime.date(start.year, start.month, last_day_of_month)
    return (start, end)


def current_month_boundaries():
    """
    Return a tuple composed of the first and the last day
    of the current month, as datetime objects

    Note: set timezone when providing! Otherwise efault timezone will be UTC
    If th server is actually in a different time zone, beware off-by-one
    month errors when using this function
    """
    start = datetime.date.today().replace(day=1)
    month_range = calendar.monthrange(start.year, start.month)
    last_day_of_month = month_range[1]
    end = datetime.date(start.year, start.month, last_day_of_month)
    return (start, end)


def generate_monthly_balance_graph(data, goals):
    """
    Write syncronously the graph to a file
    Return the graph representing whether a graph was generated or not
    """
    if len(data) > 1:
        # Write graph to file
        # NOTE: this is syncrous!
        # NOTE: require static/images folder to exist, have privileges, etc
        dates = []
        amounts = []
        for val in data:
            dates.append(val['date'])
            try:
                amounts.append(val['actual_amount'])
            except (AttributeError, NameError, KeyError) as e:
                print("You've forgot to add actual_amount somewhere (bar)")
                amounts.append(val['amount'])
        return plot.generateGraph(dates, amounts, goals)

    return False


def generate_current_monthly_balance_pie_graph(data):
    """
    Return the graph and returns the data in base64
    Return boolean representing whether a graph was generated or not
    """
    if len(data) > 1:
        # Write graph to file
        # NOTE: this is syncrous!
        # NOTE: require static/images folder to exist, have privileges, etc
        labels = []
        values = []
        for mb in filter(lambda y: y.amount > 0, data):
            labels.append(mb.category.text)
            # TODO: remove this once all places calling this function are
            # passing monthly budgets with actual_ammount attribute
            try:
                values.append(mb.actual_amount)
            except AttributeError as e:
                print("You've forgot to add actual_amount somewhere (pie)")
                values.append(mb.amount)

        return plot.generatePieGraph(labels, values)
    return False


# Credits https://stackoverflow.com/a/58612038
def findInList(List, item):
    """
    Return the index of item inside List, or -1 if not found
    """
    try:
        return List.index(item)
    except ValueError:
        return -1


def generate_current_month_expenses_pie_graph(data):
    """
    Return the graph and returns the data in base64
    Return boolean representing whether a graph was generated or not
    """
    if len(data) > 1:
        # Write graph to file
        # NOTE: this is syncrous!
        # NOTE: require static/images folder to exist, have privileges, etc
        labels = []
        values = []

        # NOTE: this ugly block saves us one query... is it worth it?
        for mb in filter(lambda y: y.amount > 0, data):
            index = findInList(labels, mb.category.text)
            if index == -1:
                labels.append(mb.category.text)
                values.append(mb.amount)
            else:
                values[index] = values[index] + mb.amount

        return plot.generatePieGraph(labels, values)
    return False


def append_year_and_month_to_url(obj, named_url, delete=False):
    """
    Return an url with obj's date appended in YYYY-mm format
    """
    format_str = '%Y-%m'
    date_ym = obj.date.strftime(format_str)
    view_url = reverse(named_url)
    redirect_url = f"{view_url}/{date_ym}"
    if delete:
        redirect_url = f"{redirect_url}?delete=1"
    return redirect_url


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
        return reverse('expenses')


class ExpenseListView(ListView):
    model = m.Expense

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start = yymm_date = self.kwargs.get('start', None)
        end = yymm_date = self.kwargs.get('end', None)

        # Toggle delete buttons
        show_delete = self.request.GET.get('delete', False) == '1'
        context['show_delete'] = show_delete

        # TODO: this cose is exactly the same as get_queryset(),memoized it
        if end is None:
            (start, end) = get_month_boundaries(start)
        else:
            format_str = '%Y-%m-%d'
            start = datetime.datetime.strptime(start, format_str).date()

        # TODO: this cose is exactly the same as get_queryset(), memoized it!
        # TODO refactor these queries after reading Django annotation docs
        # and aggregation
        expenses = m.Expense.objects.filter(date__range=(start, end)) \
                    .order_by('-date', '-id')
        expenses_sum = expenses.aggregate(Sum('amount'))['amount__sum']
        pie_graph = generate_current_month_expenses_pie_graph(expenses)
        context['pie_graph'] = pie_graph
        return context

    def get_queryset(self):
        start = yymm_date = self.kwargs.get('start', None)
        end = yymm_date = self.kwargs.get('end', None)

        # TODO: this cose is exactly the same as get_context_data(),memoized it
        if end is None:
            (start, end) = get_month_boundaries(start)
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
            monthly_budgets = m.MonthlyBudget.objects.all()
        else:
            complete_date = f"{yymm_date}-01"
            monthly_budgets = m.MonthlyBudget.objects.filter(date=complete_date)
        return monthly_budgets


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
        if end is None:
            (start, end) = get_month_boundaries(start)
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


@require_http_methods(["GET"])
def home_page(request):
    """
    Display the home page
    """
    currency = os.getenv("CURRENCY")
    (start, end) = current_month_boundaries()
    rate = os.getenv("EXCHANGE_RATE")
    # Get current and preivous month balances
    current_balance = get_total_of_monthly_balances(start)
    prev_month = get_previous_month_first_day_date(start)
    starting_balance = get_total_of_monthly_balances(prev_month)

    # Fetch previous month data to comapre it with the current month's
    prev_mb = m.MonthlyBalance.objects.select_related('category'). \
        annotate(actual_amount=Case(
          # The annotation 'amount' conflicts with a field on the model.
          When(category__is_foreign_currency=False, then='amount'),
          When(category__is_foreign_currency=True, then=F('amount') * rate)
        )).filter(date=prev_month).order_by('category_id')

    prev_mb_total = prev_mb.aggregate(correct_sum=Sum(Case(
      When(category__is_foreign_currency=False, then='amount'),
      When(category__is_foreign_currency=True, then=F('amount') * rate)
    )))['correct_sum']

    # Display pie graph
    # TODO: we could turn "actual_amount" into amount if we find how to
    #       overwrite/shadow the amount field
    current_mb = m.MonthlyBalance.objects.select_related('category'). \
        annotate(actual_amount=Case(
          # The annotation 'amount' conflicts with a field on the model.
          When(category__is_foreign_currency=False, then='amount'),
          When(category__is_foreign_currency=True, then=F('amount') * rate)
        )).filter(date=start).order_by('category_id')

    current_mb_total = current_mb.aggregate(correct_sum=Sum(Case(
      When(category__is_foreign_currency=False, then='amount'),
      When(category__is_foreign_currency=True, then=F('amount') * rate)
    )))['correct_sum']

    pie_graph = generate_current_monthly_balance_pie_graph(current_mb)

    if current_mb_total is None:
        current_mb_total = 0
        two_months_diff = 0
        two_months_diff_perc = 0
    elif prev_mb_total is None:
        two_months_diff = current_mb_total
        two_months_diff_perc = None
    else:
        two_months_diff = current_mb_total - prev_mb_total
        two_months_diff_perc = (current_mb_total / prev_mb_total * 100) - 100
        # Truncate to two decimals
        two_months_diff_perc = '%.2f' % (two_months_diff_perc)

    # Display bar graph (only draw "active" goals)
    goals = m.Goal.objects.filter(is_archived=False)
    # Calculate time to complete each goal given the last two months difference
    for goal in goals:
        if current_mb_total >= goal.amount:
            goal.months_to_go = 0
        elif two_months_diff < 0:
            # Handle case where the balance has decreased
            goal.months_to_go = None
        else:
            diff = goal.amount - current_mb_total
            try:
                months_to_go = diff / two_months_diff
            except ZeroDivisionError:
                months_to_go = 0
            goal.months_to_go = math.ceil(months_to_go)

    mb = m.MonthlyBalance.objects.select_related('category').values('date'). \
        annotate(actual_amount=Sum(Case(
          When(category__is_foreign_currency=False, then='amount'),
          When(category__is_foreign_currency=True, then=F('amount') * rate)
        ))).order_by('date')
    bar_graph = generate_monthly_balance_graph(mb, goals)

    # Fetch expenses and related categories
    categories = m.Category.objects.all()
    for cat in categories:
        expenses = m.Expense.objects.filter(category_id=cat.id). \
                   filter(date__range=(start, end))
        expenses_sum = expenses.aggregate(Sum('amount'))['amount__sum']
        cat.total = expenses_sum
        cat.mb = cat.monthlybudget_set.filter(date=start).first()

    # Fetch income and related categories
    income_categories = m.IncomeCategory.objects.all()
    for inc_c in income_categories:
        income = m.Income.objects.filter(category_id=inc_c.id). \
            filter(date__range=(start, end))
        income_sum = income.aggregate(Sum('amount'))['amount__sum']
        inc_c.total = income_sum

    return render(request, 'home.html', {
        'categories': categories,
        'income_categories': income_categories,
        'current_balance': current_balance,
        'starting_balance': starting_balance,
        # TODO: do this on the template side
        'currency': currency,
        'bar_graph': bar_graph,
        'pie_graph': pie_graph,
        'current_mb': current_mb,
        'current_mb_total': current_mb_total,
        'prev_mb': prev_mb,
        'prev_mb_total': prev_mb_total,
        'two_months_diff': two_months_diff,
        'two_months_diff_perc': two_months_diff_perc,
        'goals': goals,
    })


@require_http_methods(["GET", "POST"])
def monthly_balances_page(request, date=None):
    """
    Display the monthly balance page
    """
    errors = None
    if request.method == 'POST':
        try:
            form = f.MonthlyBalanceForm(data=request.POST)
            if form.is_valid():
                form.full_clean()
                form.save()
                redirect_url = reverse('monthly_balances')
                return redirect(redirect_url)
            else:
                errors = form.errors
        except ValidationError:
            errors = form.errors

    # Toggle delete buttons
    show_delete = request.GET.get('delete', False) == '1'
    rate = os.getenv("EXCHANGE_RATE")
    total = None
    bar_graph = False
    if date is None:
        mb = m.MonthlyBalance.objects.select_related('category'). \
            values('date').order_by('date'). \
            annotate(amount=Sum(Case(
              When(category__is_foreign_currency=False, then='amount'),
              When(category__is_foreign_currency=True, then=F('amount') * rate)
            )))
        # Display only not archived goals
        goals = m.Goal.objects.filter(is_archived=False)
        bar_graph = generate_monthly_balance_graph(mb, goals)
    else:
        complete_date = f"{date}-01"
        # Do NOT converto to local currency in here
        mb = m.MonthlyBalance.objects.select_related('category'). \
            filter(date=complete_date).order_by('date')

    total = mb.aggregate(Sum('amount'))['amount__sum']

    return render(request, 'monthly_balances.html', {
      'monthly_balance': mb,
      'bar_graph': bar_graph,
      'form': f.MonthlyBalanceForm(),
      'total': total,
      'show_delete': show_delete,
      'errors': errors
    })


@require_http_methods(["POST"])
def delete_monthly_balance_page(request, id=None):
    """
    Delete a monthly balance
    """
    errors = None
    mb = get_object_or_404(m.MonthlyBalance, pk=id)
    # Since we delete a monthly balance, the previous page was showing buttons
    show_delete = True
    redirect_url = append_year_and_month_to_url(mb, 'monthly_balances',
                                                show_delete)
    mb.delete()
    return redirect(redirect_url)


@require_http_methods(["GET", "POST"])
def monthly_balances_edit_page(request, id=None):
    errors = None
    mb = get_object_or_404(m.MonthlyBalance, pk=id)

    if request.method == 'POST':
        try:
            form = f.MonthlyBalanceForm(data=request.POST, instance=mb)
            if form.is_valid():
                form.full_clean()
                form.save()

                redirect_url = append_year_and_month_to_url(mb,
                                                            'monthly_balances')
                return redirect(redirect_url)
            else:
                errors = form.errors
        except ValidationError:
            errors = form.errors
    else:
        form = f.MonthlyBalanceForm(instance=mb)
        print(type(form.errors))

    return render(request, 'edit_monthly_balances.html', {
      'id': id,
      'form': form,
      'errors': errors
    })
