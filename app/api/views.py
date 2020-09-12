from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

import budgets.models as m
from budgets.serializers import CategorySerializer

###############################################################################
# API
###############################################################################


@login_required
@api_view(['GET'])
# @renderer_classes([JSONRenderer])
def api_categories(request):
    """
    List all categories
    """
    categories = m.Category.objects.filter(
                 created_by=request.user).order_by('id')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
