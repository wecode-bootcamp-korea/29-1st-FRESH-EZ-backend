import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freshez.settings")
django.setup()

from product.models import PurchaseMethod

CSV_PATH_PRODUCTS = './CSV_Purchase_method.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            method_name = row[0]
        PurchaseMethod.objects.create(
            name=method_name
        )
    print("Done")