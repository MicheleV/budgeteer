# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.shortcuts import render, redirect
# Docs at https://docs.djangoproject.com/en/2.2/topics/http/decorators/
from django.views.decorators.http import require_http_methods
from budgets.models import Category,Expense, MonthlyBudget

@require_http_methods(["GET"])
def home_page(request):
  return render(request, 'home.html')

@require_http_methods(["GET", "POST"])
def categories_page(request):
  category_name = request.POST.get("category_text",None)
  # TODO, this should throw 30X instead of redirecting and ignoring the missing param
  if request.method == 'POST' and category_name:
    Category.objects.create(text=category_name)
    return redirect('/categories')

  categories = Category.objects.all()
  return render(request, 'categories.html', {'categories':categories})

@require_http_methods(["GET"])
def expenses_page(request):
  # TODO refactor these queries after reading Django docs about annotation and aggregation
  categories = Category.objects.all()
  for cat in categories:
    expenses = Expense.objects.filter(category_id=cat.id)
    expenses_sum = sum(ex.amount for ex in expenses)
    cat.total = expenses_sum

  expenses = Expense.objects.all()

  return render(request, 'expenses.html', {
    'categories': categories,
    'expenses': expenses
  })

@require_http_methods(["POST"])
def new_expense_page(request):
  expense = Expense.objects.create(
    amount=request.POST.get("expense_amount",None),
    category_id=request.POST.get("category",None),
    spended_date=request.POST.get("release_date",None),
    note=request.POST.get("note",None),
  )
  expense.full_clean()
  expense.save()
  return redirect('/expenses')

@require_http_methods(["POST"])
def new_monthly_budgets_page(request):
  budget = MonthlyBudget.objects.create(
    amount=request.POST.get("budget_amount",None),
    category_id=request.POST.get("category",None),
    date=request.POST.get("budget_date",None),
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
