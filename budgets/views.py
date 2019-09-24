# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.urls import reverse
from budgets.models import Category, Expense, MonthlyBudget
from budgets.forms import CategoryForm, ExpenseForm, MonthlyBudgetForm

import datetime
import calendar


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
    (start, end) = current_month_boundaries()
    # TODO check whether prefetch_related can be used for related models
    categories = Category.objects.all()
    for cat in categories:
        # TODO refactor these queries after reading Django docs about
        # annotation and aggregation
        expenses = Expense.objects.filter(category_id=cat.id). \
                   filter(spended_date__range=(start, end))
        expenses_sum = sum(ex.amount for ex in expenses)
        cat.total = expenses_sum
        cat.mb = cat.monthlybudget_set.filter(date=start).first()
    return render(request, 'home.html', {
        'categories': categories,
    })


@require_http_methods(["GET", "POST"])
def categories_page(request):
    errors = None
    if request.method == 'POST':
        try:
            form = CategoryForm(data=request.POST)
            if form.is_valid():
                form.save()
                form.full_clean()
                redirect_url = reverse('categories')
                return redirect(redirect_url)
            else:
                errors = form.errors
        except ValidationError:
            errors = form.errors

    categories = Category.objects.all()
    return render(request,
                  'categories.html',
                  {'categories': categories,
                   'errors': errors,
                   'form': CategoryForm()})


@require_http_methods(["GET", "POST"])
def expenses_page(request, date=None):
    errors = None
    if request.method == 'POST':
        try:
            form = ExpenseForm(data=request.POST)
            if form.is_valid():
                form.save()
                form.full_clean()
            else:
                errors = form.errors
        except ValidationError:
            errors = form.errors

    # TODO: use the date parameter if present to filter
    (start, end) = current_month_boundaries()
    # TODO refactor these queries after reading Django docs about annotation
    # and aggregation
    categories = Category.objects.all()
    expenses = Expense.objects.filter(spended_date__range=(start, end))
    return render(request, 'expenses.html', {
        'categories': categories,
        'expenses': expenses,
        'form': ExpenseForm(),
        'errors': errors,
    })


@require_http_methods(["GET", "POST"])
def monthly_budgets_page(request, date=None):
    # TODO: use the date parameter if present to filter
    errors = None
    if request.method == 'POST':
        try:
            form = MonthlyBudgetForm(data=request.POST)
            if form.is_valid():
                form.save()
                form.full_clean()
            else:
                errors = form.errors
        except ValidationError:
            errors = form.errors

    categories = Category.objects.all()
    monthly_budgets = MonthlyBudget.objects.all()
    return render(request, 'monthly_budgets.html', {
      'categories': categories,
      'monthly_budgets': monthly_budgets,
      'form': MonthlyBudgetForm(),
      'errors': errors
    })
