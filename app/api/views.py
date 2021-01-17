from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from rest_framework.decorators import api_view
from rest_framework.response import Response

import budgets.models as m
from budgets.serializers import CategorySerializer
from budgets.serializers import ExpenseSerializer
from budgets.serializers import MonthlyBalanceCategorySerializer
from budgets.serializers import MonthlyBalanceSerializer
from budgets.views_utils import current_month_boundaries

###############################################################################
# API
###############################################################################


@login_required
@api_view(['GET'])
# @renderer_classes([JSONRenderer])
def all_categories(request):
    """
    List all categories
    """
    filters = {
      'created_by': request.user
    }

    # Case insensitive: "where name ILIKE '%xxx%'"
    if request.GET.get('name'):
        filters['text__icontains'] = request.GET['name']

    categories = m.Category.objects.filter(**filters).order_by('id')  # pylint: disable=E1101; # noqa
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@login_required
@api_view(['GET'])
def all_expenses(request):
    """
    List all expenses
    """
    filters = {
      'created_by': request.user
    }
    # TODO: add value validation to each parameter

    # Filter by single category
    if request.GET.get('category_id'):
        filters['category__id'] = request.GET['category_id']
    elif request.GET.get('category_name'):
        filters['category__text'] = request.GET['category_name']

    # NOTE: filter by date: both extremes included
    if request.GET.get('start'):
        filters['date__gte'] = request.GET['start']

    if request.GET.get('end'):
        filters['date__lte'] = request.GET['end']

    # Case insensitive: "where note ILIKE '%xxx%'"
    if request.GET.get('note'):
        filters['note__icontains'] = request.GET['note']

    queryset = m.Expense.objects.select_related(  # pylint: disable=E1101; # noqa
                  'category').filter(**filters).order_by('id')

    # Return 100 results by default
    # Return everything if "huge_page" param is set
    if not request.GET.get('huge_page'):
        paginator = Paginator(queryset, 100)
        page = request.query_params.get('page')

        try:
            expenses = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            expenses = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            expenses = paginator.page(paginator.num_pages)

        serializer = ExpenseSerializer(expenses, many=True)
    else:
        serializer = ExpenseSerializer(queryset, many=True)

    return Response(serializer.data)


@login_required
@api_view(['GET'])
def monthly_balance_categories(request):
    """
    List all monthly balance categories
    """
    filters = {
      'created_by': request.user
    }

    # Case insensitive: "where name ILIKE '%xxx%'"
    if request.GET.get('name'):
        filters['text__icontains'] = request.GET['name']

    categories = m.MonthlyBalanceCategory.objects.filter(**filters).order_by('id')  # pylint: disable=E1101; # noqa
    serializer = MonthlyBalanceCategorySerializer(categories, many=True)
    return Response(serializer.data)


@login_required
@api_view(['GET'])
def monthly_balances(request):
    """
    List all monthly balances for a given month
    """
    filters = {
      'created_by': request.user
    }

    # Show current month balances by default
    if request.GET.get('date'):
        filters['date'] = request.GET['date']
    else:
        filters['date'] = current_month_boundaries()[0]

    mb = m.MonthlyBalance.objects.filter(**filters).order_by('id')  # pylint: disable=C0103,E1101; # noqa
    serializer = MonthlyBalanceSerializer(mb, many=True)
    return Response(serializer.data)
