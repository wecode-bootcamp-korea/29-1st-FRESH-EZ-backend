import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freshez.settings")
django.setup()

from product.models import ProductImage, Product

CSV_PATH_PRODUCTS = './CSV_Google_product_image.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    i = 1
    for row in data_reader:
        google_image_url = row[0]
        product_instance = Product.objects.get(id=i)

        ProductImage.objects.create(
            product=product_instance,
            image_url=google_image_url,
        )

        i += 1
    print("Done")