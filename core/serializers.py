from drf_jsonmask.serializers import FieldsListSerializerMixin
from rest_framework import serializers

from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OptimizedOrderSerializer(FieldsListSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'


class OptimizedOrderItemSerializer(FieldsListSerializerMixin, serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'
