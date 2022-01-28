from random import *
import random

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from product.models import Product


class ProductDetailView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        productimage = product.productimage_set.all()
        title_image_url = productimage[0].image_url
        str_title_image_url = str(title_image_url)

        allergy_list = [product_allergy.allergy.name for product_allergy in product.productallergy_set.all()]

        return JsonResponse({
            "message" : "SUCCESS",
            "name" : product.name,
            "category" : product.category.name,
            "price" : product.price,
            "desc" : product.description,
            "allergy" : allergy_list,
            "title_image_url" : str_title_image_url,
        }, status=200)
