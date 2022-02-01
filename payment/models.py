from django.db import models

from subscription.models import Subscription


class Receipt(models.Model):
    invoice_number = models.IntegerField()
    subscription   = models.ForeignKey(Subscription, on_delete=models.DO_NOTHING, null=False, related_name='receipt')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'receipts'
