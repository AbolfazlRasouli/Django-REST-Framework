from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer



# 1
# def product_list(request: HttpRequest):
#     return HttpResponse('salsa')


# ===========================/___2___/=================================
# @api_view()
# def product_list(request):
#     return Response('salsa')
#
#
# @api_view()
# def product_detail(request, pk):
#     return Response(pk)


# ===========================/___3___/=================================
# @api_view()
# def product_detail(request, pk):
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)
#

@api_view()
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


# ===========================/___4___/=================================
@api_view()
def product_list(request):
    product_queryset = Product.objects.all()
    serializer = ProductSerializer(product_queryset, many=True)
    return Response(serializer.data)