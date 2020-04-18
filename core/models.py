from django.db import models


class Order(models.Model):
    customer = models.CharField(max_length=100)
    document = models.CharField(max_length=100)
    birth_date = models.DateField()
    address = models.CharField(max_length=100)
    address_number = models.IntegerField()
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    state_initials = models.CharField(max_length=100)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
