from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('carts', views.CartViewSet)

product_routers = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_routers.register('comments', views.CommentViewSet, basename='product_comment')

cart_item_routers = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_item_routers.register('items', views.CartItemViewSet, basename='cart_items')



# urlpatterns = router.urls + product_routers.urls


urlpatterns = [
    path('', include(router.urls)),

] + product_routers.urls + cart_item_routers.urls


