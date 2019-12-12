from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),

    path('categories', views.categories_page, name='categories'),
    path('new_category', views.categories_page, name='new_category'),

    path('expenses', views.expenses_page, name='expenses'),
    # TODO this currently also matches
    # 'expenses/2019-12-01-any-amount-of-characters'
    re_path(r'expenses/(?P<date>(19|20)[0-9]{2}-(0[1-9]|1[012]))',
            views.expenses_page, name='expenses'),
    path('new_expense', views.expenses_page, name='new_expense'),

    path('monthly_budgets',
         views.monthly_budgets_page, name='monthly_budgets'),
    # TODO this currently also matches
    # 'monthly_budgets/2019-12-01-any-amount-of-characters'
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

    # TODO this currently also matches
    # 'monthly_balances/2019-12-01-any-amount-of-characters'
    path('monthly_balances', views.monthly_balances_page,
         name='monthly_balances'),
    re_path('monthly_balances/(?P<date>(19|20)[0-9]{2}-(0[1-9]|1[012]))',
            views.monthly_balances_page, name='monthly_balances'),
    path('new_monthly_balance', views.monthly_balances_page,
         name='new_monthly_balance'),

    path('api/', views.api_categories)
]
