from datetime import datetime
from email.mime import message
from enum import auto
from tkinter import CASCADE
from django.db import models
from django.forms import DateTimeField
from django.core.validators import MinValueValidator

# Create your models here.


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=20)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=20)
    partner_Number = models.CharField(max_length=6)
    brand = models.CharField(max_length=20)
    made = models.CharField(max_length=20)
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2,
        validators=[MinValueValidator(1)])
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True)
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'BRONZE'),
        (MEMBERSHIP_SILVER, 'SILVER'),
        (MEMBERSHIP_GOLD, 'GOLD')
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=50, unique=True)
    phone = models.PositiveBigIntegerField()
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self) -> str:
        return f'{self.first_name}{self.last_name}'

    class Meta:
        ordering = ['first_name', 'last_name']


# order model


class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'

    PAYMENT_STATUS = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed')
    ]

    place_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


# order items models

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

# address model


class Address(models.Model):
    street = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    zip = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

# cart class


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


# class for cartItem

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
