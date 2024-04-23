from decimal import Decimal
from rest_framework import serializers


DOLORS_TO_RIALS = 500000


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255, source='name')
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    inventory = serializers.IntegerField()
    price_rials = serializers.SerializerMethodField()
    unit_price_after_tax = serializers.SerializerMethodField()
    # unit_price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def get_price_rials(self, product):
        return int(product.price * DOLORS_TO_RIALS)

    def get_unit_price_after_tax(self, product):
        return round(product.price * Decimal(1.09), 2)