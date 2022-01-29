import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freshez.settings")
django.setup()

from product.models import Category

CSV_PATH_PRODUCTS = './CSV_Category.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            category_name = row[0]
        Category.objects.create(
            name=category_name
        )
    print("Done")