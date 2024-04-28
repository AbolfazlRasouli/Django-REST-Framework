from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views
# from rest_framework_nested import routers


# urlpatterns = [
#     path('product/', views.ProductList.as_view(), name='product_list'),
#     path('product/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
#     path('category/', views.CategoryList.as_view(), name='category-list'),
#     path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
# ]

# ====================================  SimpleRouter() =========================================

# router = SimpleRouter()
# router.register('products', views.ProductViewSet, basename='product')
# router.register('categories', views.CategoryViewSet, basename='category')
#
# # urlpatterns = router.urls
# urlpatterns = [
#     path('', include(router.urls))
# ]

# ====================================  DefaultRouter() =========================================
router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls))
]



