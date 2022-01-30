
from django.db import models

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
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class UserAllergy(models.Model):
    allergy = models.ForeignKey(Allergy, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_allergies'