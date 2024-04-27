from decimal import Decimal
from rest_framework import serializers
from django.utils.text import slugify
from .models import Category, Product

DOLORS_TO_RIALS = 500000

# ===========================/___1___/=================================
# class CategorySerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     description = serializers.CharField(max_length=500)


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     # name = serializers.CharField(max_length=255)
#     title = serializers.CharField(max_length=255, source='name')
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory = serializers.IntegerField()
#
#     price_rials = serializers.SerializerMethodField()
#     unit_price_after_tax = serializers.SerializerMethodField()
#     # unit_price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#
#     # category = serializers.PrimaryKeyRelatedField(
#     #         queryset=Category.objects.all()
#     #     )
#     # category = serializers.StringRelatedField()
#     # category = CategorySerializer()
#     category = serializers.HyperlinkedRelatedField(
#         queryset=Category.objects.all(),
#         view_name='category-detail'
#     )
#
#     def get_price_rials(self, product):
#         return int(product.price * DOLORS_TO_RIALS)
#
#     def get_unit_price_after_tax(self, product):
#         return round(product.price * Decimal(1.09), 2)


# ===========================/___2___/=================================

class CategorySerializer(serializers.ModelSerializer):
    name_of_products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'name_of_products']

    def get_name_of_products(self, category):
        return category.products.count()


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
    #     product.slug = slugify(product.name)
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     # instance.inventory = 0
    #     instance.inventory = validated_data.get('inventory')
    #     instance.save()
    #     return instance
