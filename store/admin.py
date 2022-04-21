

from enum import auto
from itertools import count, product
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

from tags.models import TagItem
from . import models

# Register your models here.


class TagItemInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TagItem
    extra = 0
    min_num = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    search_fields = ['title']
    inlines = [TagItemInline]
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_quantity']
    list_display = ['title', 'partner_Number',
                    'unit_price', 'quantity_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10

    @admin.display(ordering='quantity')
    def quantity_status(self, product):
        if product.quantity < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear Quantity')
    def clear_quantity(self, request, queryset):
        updated_quantity = queryset.update(quantity=0)
        self.message_user(
            request, f'{updated_quantity} products were successfully updated'
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'Last_name']
    list_display = ['first_name', 'last_name', 'membership', 'customer_orders']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10

    @admin.display(ordering='products_count')
    def customer_orders(self, customer):
        url = (reverse('admin:store_order_changelist')
               + '?'
               +
               urlencode({'customer__id': str(customer.id)})
               )
        return format_html('<a href="{}">{}</a>', url, customer.customer_orders)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            customer_orders=Count('order')
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               +
               urlencode({'collection__id': str(collection.id)})
               )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


# order admin

class orderItemsInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    min_num = 1


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [orderItemsInline]
    list_display = ['id', 'place_at', 'customer']
    list_per_page = 10
