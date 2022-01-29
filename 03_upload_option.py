import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freshez.settings")
django.setup()

from product.models import Option

CSV_PATH_PRODUCTS = './CSV_Option.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            option_name = row[0]
        Option.objects.create(
            name=option_name
        )
    print("Done")