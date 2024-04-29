
# from .pagination import DefaultPagination
from .filters import ProductFilter
from .models import Product, Category, Comment, Cart
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer, CartSerializer
from django.db.models import Count
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
        if category.products.count() > 0:
            return Response({
                'error': 'There is some products including this product . please remove them first.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)

        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        return Comment.objects.filter(product_id=product_pk).all()

    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']}

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['name', 'price', 'inventory']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        if product.order_items.count() > 0:
            return Response({
                'error': 'There is some orderitem including this product . please remove them first.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#==============================/ cart /===============================

# class CartViewSet(ModelViewSet):
#     serializer_class = CartSerializer
#     queryset = Cart.objects.all()


# class CartViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
#     serializer_class = CartSerializer
#     queryset = Cart.objects.all()

class CartViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related('items').all()
