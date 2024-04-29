from django.contrib import admin

from .models import Category, Discount, Product, Customer, Address, Order, OrderItem, Comment, Cart, CartItem
admin.site.register([Category, Discount, Product, Customer, Address, Order, OrderItem, Comment, Cart, CartItem])

