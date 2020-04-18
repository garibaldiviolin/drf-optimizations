import random
import string
from datetime import datetime

from django.core.management.base import BaseCommand

from core.models import Order, OrderItem


class Command(BaseCommand):
    help = 'Populate database'

    @staticmethod
    def random_string(string_length=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(string_length))

    @staticmethod
    def random_date(start_year, end_year):
        return datetime(
            random.randint(start_year, end_year),
            random.randint(1, 12),
            random.randint(1, 28),
        )

    def handle(self, *args, **kwargs):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()

        Order.objects.bulk_create([
            Order(
                customer=self.random_string(string_length=100),
                birth_date=self.random_date(2000, 2019),
                address=self.random_string(string_length=100),
                address_number=random.randint(0, 1000),
                neighborhood=self.random_string(string_length=100),
                city=self.random_string(string_length=100),
                state=self.random_string(string_length=100),
                state_initials=self.random_string(string_length=2),
            ) for _ in range(10_000)
        ])
        self.stdout.write("Orders created.")
        order_ids = Order.objects.values_list("id", flat=True)

        OrderItem.objects.bulk_create([
            OrderItem(
                order_id=order_id,
                description=self.random_string(string_length=100),
                price=random.randint(0, 10)
            ) for order_id in order_ids for _ in range(10)
        ])
        self.stdout.write("Orders items created.")
