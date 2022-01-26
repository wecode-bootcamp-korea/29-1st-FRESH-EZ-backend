from django.db import models

from product.models import Product
from user.models import User

class OrderStatus(models.Model):
    status = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'orders_status'

class Order(models.Model):
    order_number = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    ordered_at = models.DateTimeField(auto_now=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.DO_NOTHING, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

class OrderItemStatus(models.Model):
    status = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'orders_items_status'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=False)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=False)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    order_item_status = models.ForeignKey(OrderItemStatus, on_delete=models.DO_NOTHING, null=False)
    tracking_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders_items'

class SellingCount(models.Model):
    order = models.ForeignKey(Order,on_delete=models.DO_NOTHING, null=False)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING, null=False)

    class Meta:
        db_table = 'selling_counts'