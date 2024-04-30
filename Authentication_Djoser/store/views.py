# from .pagination import DefaultPagination
from .filters import ProductFilter
from .models import Product, Category, Comment, Cart, CartItem, Customer
from .permissions import IsAdminOrReadOnly
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer, CartSerializer, CartItemSerializer, \
    CustomerSerializer
from django.db.models import Count
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()
    permission_classes = [IsAdminOrReadOnly]

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


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related('items').all()


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    # queryset = CartItem.objects.all()

    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return CartItem.objects.select_related('product').filter(cart_id=cart_pk).all()


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT']) #, permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id=user_id)
        if request.method == 'GET':
            # if request.user.is_authenticated :
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)





















