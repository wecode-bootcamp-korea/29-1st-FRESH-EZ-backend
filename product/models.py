from django.db import models
from user.models import Allergy,User
# Create your models here.

class Option(models.Model):
    name = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'options'

class Category(models.Model):
    name = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'categories'

class Sub_Category(models.Model):
    name = models.CharField(max_length=30, null=False)
    super_category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,null=False)

class Product(models.Model):
    name = models.CharField(max_length=30, null=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,null=False)
    price = models.IntegerField(null=False)
    description = models.TextField()
    allergies = models.ForeignKey(Allergy, on_delete=models.DO_NOTHING)
    product_image = models.ImageField()
    option_image1 = models.ImageField()
    option_image2 = models.ImageField()
    option_image3 = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'cart'

class Product_Allergies_Joined(models.Model):
    allergy = models.ForeignKey(Allergy, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'product_allergies_joined'

class Options_Joined(models.Model):
    option = models.ForeignKey(Option, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'options_joined'

