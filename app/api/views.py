from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

import budgets.models as m
from budgets.serializers import CategorySerializer, ExpenseSerializer

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

    if request.GET.get('name'):
        # NOTE: result into a case insensitive SQL like statement, e.g. ILIKE '%xxx%'
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

    # NOTE: filter by date: both extremes included
    if request.GET.get('start'):
        filters['date__gte'] = request.GET['start']

    if request.GET.get('end'):
        filters['date__lte'] = request.GET['end']

    queryset = m.Expense.objects.select_related(  # pylint: disable=E1101; # noqa
                  'category').filter(**filters).order_by('id')

    # Return 100 results by default
    # Return everything if "no_paging" param is set
    if not request.GET.get('no_paging'):
        paginator = Paginator(queryset, 200)
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
