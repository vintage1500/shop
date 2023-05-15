from django.db import models
from django.db.models.fields import related
from django.template.defaulttags import comment

from accounts.models import CustomUser
from pages.models import Product

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=150)
    shipping = models.BooleanField(default=False)

    def get_total_quantity(self):
        order_products = self.orderprouct_set.all()
        return sum([product.quantity for product in order_products])

    def get_total_price(self):
        order_products = self.orderprouct_set.all()
        return sum([product.get_total_price for product in order_products])


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return self.product.price * self.quantity


class Customer(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    company_name = models.CharField(max_length=150)


class ShippingAddress(models.Model):
    country = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    town = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    comment = models.TextField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)