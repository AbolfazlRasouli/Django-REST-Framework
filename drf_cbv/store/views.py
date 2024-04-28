from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Product, Category, Comment
# from .pagination import DefaultPagination
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer
from rest_framework import status
from django.db.models import Count
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


# ========================================/____ 1 ____/=================================
# class ProductList(APIView):
#
#     def get(self, request):
#         product = Product.objects.select_related('category').all()
#         serializer = ProductSerializer(product, many=True, context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         # if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response('ok')
#         # else:
#         #     return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
#
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
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
#                 'error': 'There is some orderitem including this product . please remove them first.'},
#             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
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
#
#
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
#     def delete(self, request, pk):
#         category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
#         if category.products.count() > 0:
#             return Response({
#                 'error': 'There is some products including this product . please remove them first.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# ======================================/____ 2 ____/=====================================================

# class ProductList(ListCreateAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('category').all()
#
#     # def get_serializer_class(self):
#     #     return ProductSerializer
#
#     # def get_queryset(self):
#     #     return Product.objects.select_related('category').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('category').all()
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
#
#
# class CategoryList(ListCreateAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.prefetch_related('products').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#
#     serializer_class = CategorySerializer
#     queryset = Category.objects.prefetch_related('products').all()
#
#     def delete(self, request, pk):
#         category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
#         if category.products.count() > 0:
#             return Response({
#                 'error': 'There is some products including this product . please remove them first.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# ======================================/____ 3 ____/=====================================================
# class ProductViewSet(ModelViewSet):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('category').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#     def destroy(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         if product.order_items.count() > 0:
#             return Response({
#                 'error': 'There is some orderitem including this product . please remove them first.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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


# ======================================/____ 4 ____/=====================================================

# class ProductViewSet(ModelViewSet):
#     serializer_class = ProductSerializer
#     # queryset = Product.objects.select_related('category').all()
#
#     def get_queryset(self):
#         queryset = Product.objects.all()
#         category_id_parameter = self.request.query_params.get('category_id')
#         if category_id_parameter is not None:
#             queryset = queryset.filter(category_id=category_id_parameter)
#         return queryset
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#     def destroy(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         if product.order_items.count() > 0:
#             return Response({
#                 'error': 'There is some orderitem including this product . please remove them first.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# ======================================/____ 5 ____/=====================================================

# class ProductViewSet(ModelViewSet):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['category_id', 'inventory']
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#     def destroy(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         if product.order_items.count() > 0:
#             return Response({
#                 'error': 'There is some orderitem including this product . please remove them first.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# ======================================/____ 6 ____/=====================================================

# class ProductViewSet(ModelViewSet):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = ProductFilter
#
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#     def destroy(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         if product.order_items.count() > 0:
#             return Response({
#                 'error': 'There is some orderitem including this product . please remove them first.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#

# ======================================/____ 7 ____/=====================================================

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


# ======================================/____ 8 ____/=====================================================

# class ProductViewSet(ModelViewSet):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#     filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
#     filterset_class = ProductFilter
#     search_fields = ['name']
#     ordering_fields = ['name', 'price', 'inventory']
#     # pagination_class = PageNumberPagination
#     # pagination_class = DefaultPagination
#
#     # authentication_classes = [BasicAuthentication]
#     # permission_classes = [IsAuthenticated]
#
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#     def destroy(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         if product.order_items.count() > 0:
#             return Response({
#                 'error': 'There is some orderitem including this product . please remove them first.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)