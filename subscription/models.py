from django.db import models

class Subscription(models.Model):
    size            = models.CharField(max_length=30, null=False)
    food_day_count  = models.IntegerField()
    foot_week_count = models.IntegerField()
    foot_period     = models.IntegerField()
    food_start      = models.DateField()
    food_end        = models.DateField()
    shipping_method = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriptions'
