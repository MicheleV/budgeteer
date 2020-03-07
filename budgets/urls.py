# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import path
from django.urls import re_path

from budgets import views

urlpatterns = [
    path('', views.home_page, name='home'),

    path('categories', views.categories_page, name='categories'),
    path('new_category', views.categories_page, name='new_category'),

    path('expenses', views.expenses_page, name='expenses'),
    re_path(r'expenses/(?P<start>(19|20)[0-9]{2}-(0[1-9]|1[012]))$',
            views.expenses_page, name='expenses'),

    re_path(r'expenses/(?P<start>(19|20)[0-9]{2}-(0[1-9]|1[012])-([0-3][0-9]))/(?P<end>(19|20)[0-9]{2}-(0[1-9]|1[012])-([0-3][0-9]))$',
            views.expenses_page, name='expenses_filtered'),
    path('new_expense', views.expenses_page, name='new_expense'),
    path('delete_expense/<int:id>', views.delete_expense_page,
         name='delete_expense'),

    path('monthly_budgets',
         views.monthly_budgets_page, name='monthly_budgets'),
    re_path(r'monthly_budgets/(?P<date>(19|20)[0-9]{2}-(0[1-9]|1[012]))$',
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
    re_path('monthly_balances/(?P<date>(19|20)[0-9]{2}-(0[1-9]|1[012]))$',
            views.monthly_balances_page, name='monthly_balances'),
    path('new_monthly_balance', views.monthly_balances_page,
         name='new_monthly_balance'),
    path('edit_monthly_balance/<int:id>', views.monthly_balances_edit_page,
         name='edit_monthly_balance'),
    path('delete_monthly_balance/<int:id>', views.delete_monthly_balance_page,
         name='delete_monthly_balance'),

    # TODO: add goal related urls

    path('api/categories', views.api_categories, name='api')
]
