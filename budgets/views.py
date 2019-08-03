# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.shortcuts import render, redirect
from budgets.models import Category

def home_page(request):
  return render(request, 'home.html')

def categories_page(request):
  if request.method == 'POST':
    Category.objects.create(text=request.POST.get("category_text",""))
    return redirect('/categories')

  categories = Category.objects.all()
  return render(request, 'categories.html', {'categories':categories})

