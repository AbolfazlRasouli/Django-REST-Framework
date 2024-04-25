from django.urls import path
from . import views


urlpatterns = [

    path('product/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    # path('category/', views.category_list, name='category-list'),
    path('category/<int:pk>/', views.category_detail, name='category-detail'),

]