# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from budgets.models import Category
from budgets.models import Expense
from budgets.models import MonthlyBudget
import datetime
import calendar


def current_month_boundaries():
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
    category_name = request.POST.get("category_text", None)
    # TODO, this should throw 30X instead of redirecting and ignoring the
    # missing param
    if request.method == 'POST' and category_name:
        Category.objects.create(text=category_name)
        return redirect('/categories')

    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


# TODO set the server to JST (or to your locale) when provisioning, otherwise
# Timezone is assumed to be UTC.
# E.g. being JST +8 , the query will be off by one month
# print( Expense.objects.filter(category_id=cat.id). \
#           filter(spended_date__range=(beginning, end_date)).query)
# BETWEEN 2012-02-01 AND 2012-02-29) <---On `Wed  1 Feb 09:00:16 JST 2012`
# BETWEEN 2012-01-01 AND 2012-01-31) <--- On `Wed  1 Feb 08:59:00 JST 2012`

@require_http_methods(["GET"])
# TODO later, add a parameter to select the month
def expenses_page(request):
    (start, end) = current_month_boundaries()
    # TODO this should be programmatically as we're querying again all
    # the expenses for that month after the for loop, see jsut before
    # return statemnt
    # refactor these queries after reading Django docs about annotation and
    # aggregation
    categories = Category.objects.all()

    expenses = Expense.objects.filter(spended_date__range=(start, end))
    return render(request, 'expenses.html', {
        'categories': categories,
        'expenses': expenses
    })


@require_http_methods(["POST"])
def new_expense_page(request):
    expense = Expense.objects.create(
        amount=request.POST.get("expense_amount", None),
        category_id=request.POST.get("category", None),
        spended_date=request.POST.get("release_date", None),
        note=request.POST.get("note", None),
    )
    expense.full_clean()
    expense.save()
    return redirect('/expenses')


@require_http_methods(["POST"])
def new_monthly_budgets_page(request):
    budget = MonthlyBudget.objects.create(
        amount=request.POST.get("budget_amount", None),
        category_id=request.POST.get("category", None),
        date=request.POST.get("budget_date", None),
    )
    budget.full_clean()
    budget.save()
    return redirect('/monthly_budgets')


@require_http_methods(["GET"])
def monthly_budgets_page(request):
    categories = Category.objects.all()
    monthly_budgets = MonthlyBudget.objects.all()
    return render(request, 'monthly_budgets.html', {
      'categories': categories,
      'monthly_budgets': monthly_budgets,
    })
