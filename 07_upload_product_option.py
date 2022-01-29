import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freshez.settings")
django.setup()

from product.models import Product, Option, ProductOption

CSV_PATH_PRODUCTS = './CSV_Product_option.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            option_id = row[0]
        option_instance = Option.objects.get(id=option_id)
        product_instance = Product.objects.get(id=row[1])
        ProductOption.objects.create(
            option = option_instance,
            product = product_instance
        )
    print("Done")