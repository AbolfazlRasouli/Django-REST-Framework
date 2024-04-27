from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

# from .filters import ProductFilter
from .models import Product, Category, Comment
# from .pagination import DefaultPagination
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer
from rest_framework import status
from django.db.models import Count
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


# ========================================/____ 1 ____/=================================
class ProductList(APIView):

    def get(self, request):
        product = Product.objects.select_related('category').all()
        serializer = ProductSerializer(product, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
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


# class ProductDetail(APIView):
#
#     def get(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         if product.order_items.count() > 0:
#             return Response({
#                 'error':'There is some orderitem including this product . please remove them first.'},
#             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CategoryList(APIView):
#
#     def get(self, request):
#         category = Category.objects.prefetch_related('products').all()
#         serializer = CategorySerializer(category, many=True, context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CategoryDetail(APIView):
#
#     def get(self, request, pk):
#         category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
#         serializer = CategorySerializer(category, context={'request': request})
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
#         serializer = CategorySerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    #
    # def delete(self, request, pk):
    #     category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
    #     if category.products.count() > 0:
    #         return Response({
    #             'error': 'There is some products including this product . please remove them first.'},
    #             status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #
    #     category.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

