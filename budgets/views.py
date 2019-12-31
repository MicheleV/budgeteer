# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import budgets.models as m
import budgets.forms as f
from budgets.serializers import CategorySerializer
from graphs import plot
import datetime
import calendar


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


@require_http_methods(["GET"])
def home_page(request):
    """
    Display the home page
    """
    (start, end) = current_month_boundaries()
    # TODO check whether prefetch_related can be used for related models
    categories = m.Category.objects.all()
    for cat in categories:
        expenses = m.Expense.objects.filter(category_id=cat.id). \
                   filter(date__range=(start, end))
        expenses_sum = sum(ex.amount for ex in expenses)
        # TODO refactor the line above using aggrefate(Sum())
        # expenses_sum = expenses.aggregate(Sum('amount'))['amount__sum']
        cat.total = expenses_sum
        cat.mb = cat.monthlybudget_set.filter(date=start).first()

    # TODO this code is duplicatd from above, let's make a function for this
    income_categories = m.IncomeCategory.objects.all()
    for inc_c in income_categories:
        # TODO refactor these queries after reading Django docs about
        # annotation and aggregation
        income = m.Income.objects.filter(category_id=inc_c.id). \
            filter(date__range=(start, end))
        income_sum = sum(ex.amount for ex in income)
        inc_c.total = income_sum

    return render(request, 'home.html', {
        'categories': categories,
        'income_categories': income_categories
    })


@require_http_methods(["GET", "POST"])
def categories_page(request):
    """
    Display the categories page
    """
    errors = None
    if request.method == 'POST':
        try:
            form = f.CategoryForm(data=request.POST)
            if form.is_valid():
                form.full_clean()
                form.save()
                redirect_url = reverse('categories')
                return redirect(redirect_url)
            else:
                errors = form.errors
        except ValidationError:
            errors = form.errors

    categories = m.Category.objects.all()
    return render(request,
                  'categories.html',
                  {'categories': categories,
                   'errors': errors,
                   'form': f.CategoryForm()})


@require_http_methods(["GET", "POST"])
def expenses_page(request, date=None):
    """
    Display the expenses page
    """
    errors = None
    if request.method == 'POST':
        try:
            form = f.ExpenseForm(data=request.POST)
            if form.is_valid():
                form.full_clean()
                form.save()
            else:
                errors = form.errors
        except ValidationError:
            errors = form.errors

    (start, end) = get_month_boundaries(date)
    # TODO refactor these queries after reading Django docs about annotation
    # and aggregation
    categories = m.Category.objects.all()
    expenses = m.Expense.objects.filter(date__range=(start, end))
    return render(request, 'expenses.html', {
        'categories': categories,
        'expenses': expenses,
        'form': f.ExpenseForm(),
        'errors': errors,
        'month': start.strftime("%Y-%m")
    })


@require_http_methods(["GET", "POST"])
def monthly_budgets_page(request, date=None):
    """
    Display the mohtly budgets page
    """
    errors = None
    if request.method == 'POST':
        try:
            form = f.MonthlyBudgetForm(data=request.POST)
            if form.is_valid():
                form.full_clean()
                form.save()
                redirect_url = reverse('monthly_budgets')
                return redirect(redirect_url)
            else:
                errors = form.errors
        except ValidationError:
            errors = form.errors

    categories = m.Category.objects.all()
    if date is None:
        monthly_budgets = m.MonthlyBudget.objects.all()
    else:
        complete_date = f"{date}-01"
        monthly_budgets = m.MonthlyBudget.objects.filter(date=complete_date)
    return render(request, 'monthly_budgets.html', {
      'categories': categories,
      'monthly_budgets': monthly_budgets,
      'form': f.MonthlyBudgetForm(),
      'errors': errors
    })


@require_http_methods(["GET", "POST"])
def income_categories_page(request):
    """
    Display the income categories page
    """
    errors = None
    if request.method == 'POST':
        try:
            form = f.IncomeCategoryForm(data=request.POST)
            if form.is_valid():
                form.full_clean()
                form.save()
                redirect_url = reverse('income_categories')
                return redirect(redirect_url)
            else:
                errors = form.errors
        except ValidationError:
            errors = form.errors

    categories = m.IncomeCategory.objects.all()
    return render(request,
                  'income_categories.html',
                  {'categories': categories,
                   'errors': errors,
                   'form': f.IncomeCategoryForm()})


@require_http_methods(["GET", "POST"])
def incomes_page(request, date=None):
    """
    Display the incomes page
    """
    errors = None
    if request.method == 'POST':
        try:
            form = f.IncomeForm(data=request.POST)
            if form.is_valid():
                form.full_clean()
                form.save()
            else:
                errors = form.errors
        except ValidationError:
            errors = form.errors

    # TODO: use the date parameter if present to filter
    (start, end) = current_month_boundaries()
    # TODO refactor these queries after reading Django docs about annotation
    # and aggregation
    categories = m.IncomeCategory.objects.all()
    incomes = m.Income.objects.filter(date__range=(start, end))
    return render(request, 'incomes.html', {
        'categories': categories,
        'incomes': incomes,
        'form': f.IncomeForm(),
        'errors': errors,
    })


@require_http_methods(["GET", "POST"])
def monthly_balance_categories_page(request):
    """
    Display the mohtly balance category page
    """
    errors = None
    if request.method == 'POST':
        try:
            form = f.MonthlyBalanceCategoryForm(data=request.POST)
            if form.is_valid():
                form.full_clean()
                form.save()
                redirect_url = reverse('monthly_balance_categories')
                return redirect(redirect_url)
            else:
                errors = form.errors
        except ValidationError:
            errors = form.errors

    categories = m.MonthlyBalanceCategory.objects.all()
    return render(request,
                  'monthly_balance_categories.html',
                  {'categories': categories,
                   'errors': errors,
                   'form': f.MonthlyBalanceCategoryForm()})


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

    categories = m.MonthlyBalanceCategory.objects.all()
    total = None
    if date is None:
        mb = m.MonthlyBalance.objects.values('date').order_by('date').annotate(amount=Sum('amount'))
    else:
        complete_date = f"{date}-01"
        mb = m.MonthlyBalance.objects.values('date').filter(date=complete_date).order_by('date').annotate(amount=Sum('amount'))

    total = mb.aggregate(Sum('amount'))['amount__sum']

    # Generate the graph only if we have some data
    if len(mb) > 1:
        # Write graph to file.
        # NOTE: this is syncrous!
        # NOTE: require static/images folder to exist, have privileges, etc
        dates = []
        amounts = []
        for val in mb:
            amounts.append(val['amount'])
            dates.append(val['date'])

        plot.generateGraph(dates, amounts)

    return render(request, 'monthly_balances.html', {
      'categories': categories,
      'monthly_balance': mb,
      'form': f.MonthlyBalanceForm(),
      'total': total,
      'errors': errors
    })


@api_view(['GET'])
# @renderer_classes([JSONRenderer])
def api_categories(request):
    # return Response({"message": "Hello, world!"})
    """
    List all categories
    """
    categories = m.Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
