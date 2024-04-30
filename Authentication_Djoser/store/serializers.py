from decimal import Decimal
from rest_framework import serializers
from .models import Category, Product, Comment, Cart, CartItem
from django.utils.text import slugify

DOLORS_TO_RIALS = 500000


# class CategorySerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     description = serializers.CharField(max_length=500)

class CategorySerializer(serializers.ModelSerializer):
    # name_of_products = serializers.SerializerMethodField()
    name_of_products = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'name_of_products']

    def get_name_of_products(self, category):
        return category.products.count()


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255, source='name')
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory = serializers.IntegerField()
#     price_rials = serializers.SerializerMethodField()
#     # unit_price_after_tax = serializers.SerializerMethodField()
#     unit_price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#     # category = serializers.PrimaryKeyRelatedField(
#     #     queryset=Category.objects.all()
#     # )
#     # category = serializers.StringRelatedField()
#     # category = CategorySerializer()
#     category = serializers.HyperlinkedRelatedField(
#         queryset=Category.objects.all(),
#         view_name='category-detail'
#     )
#
#
#     def get_price_rials(self, product):
#         return int(product.price * DOLORS_TO_RIALS)
#
#     # def get_unit_price_after_tax(self, product):
#     #     return round(product.price * Decimal(1.09), 2)
#
#     def calculate_tax(self, product):
#         return round(product.price * Decimal(1.09), 2)


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, source='name')
    price = serializers.DecimalField(max_digits=6, decimal_places=2)

    # price_rials = serializers.SerializerMethodField()
    # unit_price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # category = serializers.HyperlinkedRelatedField(
    #     queryset=Category.objects.all(),
    #     view_name='category-detail'
    # )

    class Meta:
        model = Product
        # fields = ['id', 'title', 'price', 'inventory', 'price_rials', 'unit_price_after_tax', 'category']
        fields = ['id', 'title', 'price', 'category', 'description', 'inventory']

    # def get_price_rials(self, product):
    #     return int(product.price * DOLORS_TO_RIALS)

    # def calculate_tax(self, product):
    #     return round(product.price * Decimal(1.09), 2)

    def validate(self, data):
        print(data)
        if len(data['name']) < 6:
            raise serializers.ValidationError('product title length should be ..')
        return data

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.slug=slugify(product.name)
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     # instance.inventory = 0
    #     instance.inventory = validated_data.get('inventory')
    #     instance.save()
    #     return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'body']

    def create(self, validated_data):
        product_id = self.context['product_pk']
        return Comment.objects.create(product_id=product_id, **validated_data)


# =====================================/ cart serializer /==================================


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total']

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.price


class CartSerializer(serializers.ModelSerializer):
    # id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        # fields = ['id', 'created_at']
        fields = ['id', 'items', 'total_price']
        # read_only_fields = ['id', 'items']
        read_only_fields = ['id', ]

    def get_total_price(self, cart):
        return sum(item.quantity * item.product.price for item in cart.items.all())
