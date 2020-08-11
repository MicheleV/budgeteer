from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

import budgets.models as m
from budgets.serializers import CategorySerializer

###############################################################################
# API
###############################################################################

# TODO: move me inside a namespace
@api_view(['GET'])
# @renderer_classes([JSONRenderer])
def api_categories(request):
    """
    List all categories
    """
    categories = m.Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
