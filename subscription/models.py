from django.db import models

from product.models import Product, Option
from user.models import User


class Subscription(models.Model):
    user            = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    size            = models.ForeignKey(Option, on_delete=models.DO_NOTHING, null=False)
    food_day_count  = models.IntegerField()
    food_week_count = models.IntegerField()
    food_period     = models.IntegerField()
    food_start      = models.DateField()
    food_end        = models.DateField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriptions'

class SubscriptionProduct(models.Model):
    subscription = models.ForeignKey("Subscription", on_delete=models.DO_NOTHING, null=True, related_name="subscription_food")
    product      = models.ForeignKey("product.Product", on_delete=models.DO_NOTHING, null=True, related_name="subscription_food")

    class Meta:
        db_table = 'subscriptions_products'

