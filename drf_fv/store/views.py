from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


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

# @api_view()
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


# ===========================/___4___/=================================
# @api_view()
# def product_list(request):
#     product_queryset = Product.objects.all()
#     serializer = ProductSerializer(product_queryset, many=True)
#     return Response(serializer.data)


# ===========================/___5___/=================================
@api_view()
# def product_list(request):
#     product = Product.objects.select_related('category').all()
#     serializer = ProductSerializer(product, many=True, context={'request': request})
#     return Response(serializer.data)
#
#
# @api_view()
# def product_detail(request, pk):
#     product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#     serializer = ProductSerializer(product, context={'request': request})
#     return Response(serializer.data)


# ===========================/___6___/=================================
@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category, context={'request': request})
    return Response(serializer.data)


# ===========================/___7___/=================================
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        product = Product.objects.select_related('category').all()
        serializer = ProductSerializer(product, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('ok')
        # else:
        #     return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if product.order_items.count() > 0:
            return Response({
                'error':'There is some order item including this product . please remove them first.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)