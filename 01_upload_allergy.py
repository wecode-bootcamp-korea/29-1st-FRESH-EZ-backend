import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freshez.settings")
django.setup()

from user.models import Allergy

CSV_PATH_PRODUCTS = './CSV_Allergy.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            allergy_name = row[0]
        Allergy.objects.create(
            name=allergy_name
        )
    print("Done")