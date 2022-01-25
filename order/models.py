from django.db import models

# Create your models here.
from product.models import Product
from user.models import User

class Order_Status(models.Model):
    status = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'order_status'

class Order(models.Model):
    order_number = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    ordered_at = models.DateTimeField(auto_now=True)
    order_status = models.ForeignKey(Order_Status, on_delete=models.DO_NOTHING, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order'

class Order_Item_Status(models.Model):
    status = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'order_item_status'

class Order_Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=False)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=False)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    order_item_status = models.ForeignKey(Order_Item_Status, on_delete=models.DO_NOTHING, null=False)
    tracking_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_item'
