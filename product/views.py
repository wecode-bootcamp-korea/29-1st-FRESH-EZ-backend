import json
from random import *
import random

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from product.models import Product, Category
from user.models import User


class SubscribeDetailView(View):
    def post(self, request, category_id):
        category = Category.objects.get(id=category_id)
        product_instance_list = Product.objects.filter(category=category.id)
        print(product_instance_list)
        product_name_list = []
        product_image_list = []
        product_price_list = []
        product_review_count_list = []
        product_review_score_list = []

        for product in product_instance_list:
            product_name_list.append(product.name)

            productimage = product.productimage_set.all()
            title_image_url = productimage[0].image_url
            str_title_image_url = str(title_image_url)
            product_image_list.append(str_title_image_url)

            product_price_list.append(product.price)

            review_count = random.randrange(2000, 3000)
            product_review_count_list.append(review_count)

            review_score = round(uniform(1, 5), 1)
            product_review_score_list.append(review_score)

        return JsonResponse({
            "message": "SUCCESS",
            "products" : product_name_list,
            "image_list" : product_image_list,
            "price": product_price_list,
            "review_count" : product_review_count_list,
            "review_score" : product_review_score_list,
        }, status=200)