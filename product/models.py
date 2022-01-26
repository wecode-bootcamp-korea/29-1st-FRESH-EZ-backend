from django.db import models
from user.models import Allergy,User

class Option(models.Model):
    name = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'options'

class Category(models.Model):
    name = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'categories'

class Product(models.Model):
    name = models.CharField(max_length=30, null=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=False)
    price = models.IntegerField(null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

class PurchaseMethod(models.Model):
    name = models.CharField(max_length=30, null=False)
    Product = models.ForeignKey(Product, on_delete=models.DO_NOTHING,null=False)

    class Meta:
        db_table = 'purchase_methods'

class ProductPurchaseMethod(models.Model):
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING, null=False)
    purchase_method = models.ForeignKey(PurchaseMethod,on_delete=models.DO_NOTHING, null=False)

    class Meta:
        db_table = 'products_purchase_methods'

class ProductImage(models.Model):
    product_image = models.ImageField()

    class Meta:
        db_table = 'products_images'

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'cart'

class ProductAllergy(models.Model):
    allergy = models.ForeignKey(Allergy, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'products_allergies'

class ProductOption(models.Model):
    option = models.ForeignKey(Option, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'products_options'

