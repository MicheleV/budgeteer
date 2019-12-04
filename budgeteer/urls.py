"""budgeteer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from budgets import views

# Note: Regex /?P<date>(19|20)[0-9]{2}-(0[1-9]|1[012]))/
# allow only dates between 1900-01 and 2099-12
# Warning: month is always two digits (i.e. Jan -> '01', not '1')
urlpatterns = [
    path('', views.home_page, name='home'),

    path('categories', views.categories_page, name='categories'),
    path('new_category', views.categories_page, name='new_category'),

    path('expenses', views.expenses_page, name='expenses'),
    re_path(r'expenses/(?P<date>(19|20)[0-9]{2}-(0[1-9]|1[012]))',
            views.expenses_page, name='expenses'),
    path('new_expense', views.expenses_page, name='new_expense'),

    path('monthly_budgets',
         views.monthly_budgets_page, name='monthly_budgets'),
    re_path(r'monthly_budgets/(?P<date>(19|20)[0-9]{2}-(0[1-9]|1[012]))',
            views.monthly_budgets_page, name='monthly_budgets'),
    path('new_monthly_budget',
         views.monthly_budgets_page, name='new_monthly_budget'),

    path('income_categories', views.income_categories_page,
         name='income_categories'),
    path('new_income_category', views.income_categories_page,
         name='new_income_category'),
    path('incomes', views.incomes_page, name='incomes'),
    path('new_income', views.incomes_page, name='new_income'),

    path('monthly_balance_categories', views.monthly_balance_categories_page,
         name='monthly_balance_categories'),
    path('new_monthly_balance_category', views.monthly_balance_categories_page,
         name='new_monthly_balance_category'),
    path('monthly_balances', views.monthly_balances_page,
         name='monthly_balances'),
    path('new_monthly_balance', views.monthly_balances_page,
         name='new_monthly_balance'),
    path('api/', views.api_categories)
]
