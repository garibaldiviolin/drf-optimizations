from collections import OrderedDict
import sys

from django.core.paginator import Paginator
from django.db import connection
from django.utils.functional import cached_property
from drf_jsonmask.views import OptimizedQuerySetMixin, OptimizedQuerySetMixin2
from drf_jsonmask.decorators import data_predicate
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import CursorPagination, PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import (
    OrderSerializer,
    OptimizedOrderSerializer,
    OrderItemSerializer,
    OptimizedOrderItemSerializer,
)


class CustomModelViewSet(ModelViewSet):
    """def list(self, request):
        print("Queries before request={}".format(connection.queries))
        response = super().list(request)
        print("Queries after request={}".format(connection.queries))
        print("Queries len={}".format(len(connection.queries)))
        return response"""


class CustomPaginatorClass(Paginator):
    @cached_property
    def count(self):
        return sys.maxsize


# To Avoid large table count query, We can use this paginator class
class LargeTablePagination(PageNumberPagination):
    django_paginator_class = CustomPaginatorClass

    def get_paginated_response(self, data):
        return Response(
            OrderedDict([
                ('next', self.get_next_link() if len(data) == 25 else None),
                ('previous', self.get_previous_link()),
                ('results', data)
            ])
        )


# To Avoid large table count query, We can use this paginator class
class LargeTablePagination2(LimitOffsetPagination):
    @cached_property
    def count(self):
        return sys.maxsize

    def get_count(self, request):
        return self.count

    def get_paginated_response(self, data):
        return Response(
            OrderedDict([
                ('next', self.get_next_link() if len(data) == 25 else None),
                ('previous', self.get_previous_link()),
                ('results', data)
            ])
        )


class OrderViewSet(CustomModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.order_by('id')


class OptimizedOrderViewSet(OptimizedQuerySetMixin, CustomModelViewSet):
    serializer_class = OptimizedOrderSerializer
    queryset = Order.objects.order_by('id')


class OptimizedOrderViewSet2(OptimizedQuerySetMixin2, CustomModelViewSet):
    serializer_class = OptimizedOrderSerializer
    queryset = Order.objects.order_by('id')


class OptimizedOrderViewSet3(OptimizedOrderViewSet2):
    pagination_class = LargeTablePagination


class OptimizedOrderViewSet4(OptimizedOrderViewSet2):
    pagination_class = LargeTablePagination2


class OptimizedOrderViewSet5(OptimizedOrderViewSet2):
    pagination_class = CursorPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ('id',)
    ordering_fields = ('id',)


class OrderItemViewSet(CustomModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.order_by('order_id', 'id')

    def list(self, request):
        return super().list(request)


class OptimizedOrderItemViewSet(OptimizedQuerySetMixin, OrderItemViewSet):
    serializer_class = OptimizedOrderItemSerializer

    @data_predicate('order')
    def load_order(self, queryset):
        return queryset.select_related('order')


class CursorOrderItemViewSet(OptimizedOrderItemViewSet):
    serializer_class = OptimizedOrderItemSerializer
    pagination_class = CursorPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ('id',)
    ordering_fields = ('id',)

    @data_predicate('order')
    def load_order(self, queryset):
        return queryset.select_related('order')
