from django.db import models
from subscription.models import Subscription

# Create your models here.

class Allergy(models.Model):
    name = models.CharField(null=False, max_length=30)

    class Meta:
        db_table = 'allergies'

class User(models.Model):
    email        = models.EmailField(null=False, unique=True)
    password     = models.CharField(null=False, max_length=500)
    name         = models.CharField(null=False, max_length=30)
    nickname     = models.CharField(null=False, max_length=30)
    phone        =  models.CharField(null=False, max_length=30)
    birth        = models.DateField(null=False)
    sex          = models.CharField(null=False, max_length=30)
    subscription = models.ForeignKey(Subscription, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class User_Allergies_Joined(models.Model):
    allergy = models.ForeignKey(Allergy, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_allergies_joined'



