# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.shortcuts import render, redirect
# Docs at https://docs.djangoproject.com/en/2.2/topics/http/decorators/
from django.views.decorators.http import require_http_methods
from budgets.models import Category,Expense

@require_http_methods(["GET"])
def home_page(request):
  return render(request, 'home.html')

@require_http_methods(["GET", "POST"])
def categories_page(request):
  if request.method == 'POST':
    Category.objects.create(text=request.POST.get("category_text",""))
    return redirect('/categories')

  categories = Category.objects.all()
  return render(request, 'categories.html', {'categories':categories})

@require_http_methods(["GET"])
def expenses_page(request):
  categories = Category.objects.all()
  expenses = Expense.objects.all()
  return render(request, 'expenses.html', {
    'categories': categories,
    'expenses': expenses
  })

@require_http_methods(["POST"])
def new_expense_page(request):
  Expense.objects.create(
    amount=request.POST.get("expense_amount",None),
    category_id=request.POST.get("category",None),
    spended_date=request.POST.get("release_date",None),
    note=request.POST.get("note",None),
  )

  return redirect('/expenses')
