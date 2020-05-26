# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import path
from django.urls import re_path

from budgets import views

urlpatterns = [
    # Class based routes #
    path('categories', views.CategoryListView.as_view(), name='categories'),
    path('categories/create', views.CategoryCreateView.as_view(),
         name='categories_create'),

    # Expenses
    path('expenses/create', views.ExpenseCreateView.as_view(),
         name='expenses_create'),
    # Show all expenses
    path('expenses', views.ExpenseListView.as_view(), name='expenses'),
    # Show expensece since YYYY-mm
    re_path(r'expenses/(?P<start>(19|20)[0-9]{2}-(0[1-9]|1[012]))$',
            views.ExpenseListView.as_view(), name='expenses'),
    # Show expensece between YYYY-mm-dd and YYYY-mm-dd (extremes included)
    re_path(r'expenses/(?P<start>(19|20)[0-9]{2}-(0[1-9]|1[012])-([0-3][0-9]))/(?P<end>(19|20)[0-9]{2}-(0[1-9]|1[012])-([0-3][0-9]))$',
            views.ExpenseListView.as_view(), name='expenses_filtered'),
    path('expenses/delete/<int:pk>', views.ExpenseDeleteView.as_view(),
         name='expenses_delete'),

    # Goals
    path('goals/create', views.GoalCreateView.as_view(), name='goals_create'),
    path('goals', views.GoalListView.as_view(), name='goals'),
    path('goals/<int:pk>', views.GoalDetailView.as_view(),
         name='goals_detail'),

    # Monthly balance categories
    path('monthly_balance_categories/create',
         views.MonthlyBalanceCategoryCreateView.as_view(),
         name='new_monthly_balance_category'),

    path('monthly_balance_categories',
         views.MonthlyBalanceCategoryView.as_view(),
         name='monthly_balance_categories'),

    path('monthly_balance_categories/<int:pk>',
         views.MonthlyBalanceCategoryDetailView.as_view(),
         name='monthly_balance_categories_details'),

    # Monthly balances
    path('monthly_balances/create', views.MonthlyBalancesCreateView.as_view(),
         name='monthly_balances_create'),

    path('monthly_balances/multiple_create', views.multiple_new_product,
         name='monthly_balances_multiple_create'),


    path('monthly_balances', views.MonthlyBalancesView.as_view(),
         name='monthly_balances'),

    path('edit_monthly_balance/<int:pk>',
         views.MonthlyBalanceUpdateView.as_view(),
         name='edit_monthly_balance'),

    path('monthly_balances/delete/<int:pk>',
         views.MonthlyBalanceDeleteView.as_view(),
         name='monthly_balances_delete'),

    # Show monthly balances breakdonw by date (YYYY-mm)
    re_path('monthly_balances/(?P<date>(19|20)[0-9]{2}-(0[1-9]|1[012]))$',
            views.MonthlyBalancesSingleMonthView.as_view(),
            name='monthly_balances'),

    # Income categories
    path('income_categories/create', views.IncomeCategoryCreateView.as_view(),
         name='income_categories_create'),
    path('income_categories', views.IncomeCategoryView.as_view(),
         name='income_categories'),

    # Incomes
    path('incomes/create', views.IncomCreateView.as_view(),
         name='incomes_create'),
    path('incomes', views.IncomeView.as_view(), name='incomes'),

    # Monthly budgets
    path('monthly_budgets',
         views.MonthlyBudgetListView.as_view(), name='monthly_budgets'),

    # Monthly budgets for a given month
    re_path(r'monthly_budgets/(?P<date>(19|20)[0-9]{2}-(0[1-9]|1[012]))$',
            views.MonthlyBudgetListView.as_view(), name='monthly_budgets'),
    path('monthly_budgets/create',
         views.MonthlyBudgetsCreateView.as_view(),
         name='monthly_budgets_create'),
    path('monthly_budgets/<int:pk>', views.MonthlyBudgetDetailView.as_view(),
         name='monthly_budgets_detail'),

    # API #
    path('api/categories', views.api_categories, name='api'),

    # Function based routes #
    path('', views.home_page, name='home'),
]
