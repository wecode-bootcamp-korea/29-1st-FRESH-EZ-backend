import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freshez.settings")
django.setup()

from user.models import Allergy
from product.models import Product, Category

CSV_PATH_PRODUCTS = './Product.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[3]:
            category_id = row[3]
        category_instance = Category.objects.get(id=category_id)
        Product.objects.create(
            name=row[0],
            price=row[1],
            description=row[2],
            category=category_instance,
        )
    print("Done")