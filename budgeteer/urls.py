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
from django.urls import path
from budgets import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('categories', views.categories_page, name='categories'),
    path('new_category', views.categories_page, name='new_category'),
    path('expenses', views.expenses_page, name='expenses'),
    path('new_expense', views.new_expense_page, name='new_expense'),
]
