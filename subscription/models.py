from django.db import models

from product.models import Product
from user.models import User


class Subscription(models.Model):
    user            = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    size            = models.CharField(max_length=30, null=False)
    food_day_count  = models.IntegerField()
    foot_week_count = models.IntegerField()
    foot_period     = models.IntegerField()
    food_start      = models.DateField()
    food_end        = models.DateField()
    shipping_method = models.IntegerField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    product         = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=False)

    class Meta:
        db_table = 'subscriptions'
