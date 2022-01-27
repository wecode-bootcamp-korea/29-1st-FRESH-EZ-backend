import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freshez.settings")
django.setup()

from user.models import Allergy
from product.models import Product, Category, ProductPurchaseMethod, PurchaseMethod, ProductAllergy

CSV_PATH_PRODUCTS = './Product_middle_table.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[1]:
            purchase_method_id = row[1]
        purchase_instance = PurchaseMethod.objects.get(id=purchase_method_id)
        product_instance = Product.objects.get(id=row[0])
        ProductPurchaseMethod.objects.create(
            product=product_instance,
            purchase_method=purchase_instance
        )

        allergy_instance = Allergy.objects.get(id=row[2])
        product_instance = Product.objects.get(id=row[3])
        ProductAllergy.objects.create(
            allergy_id=allergy_instance,
            product=product_instance
        )
    print("Done")