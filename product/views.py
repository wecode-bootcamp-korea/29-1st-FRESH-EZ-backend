import json
import datetime
import random

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.views import View

from product.models import Product
from subscription.models import Subscription, SubscriptionProduct
from user.models import User


class SubscribeOptionView(View):
    def post(self, request):
        data  = json.loads(request.body)

        user            = User.objects.get(email="wepungsan@gmail.com")
        size            = data['size']
        food_day_count  = data['food_day_count']
        food_week_count = data['food_week_count']
        food_period     = data['food_period']
        food_start      = data['food_start']

        if "product_list" in data:
            product_list = data['product_list']

        year, month, day = food_start.split("-")
        year             = int(year)
        month            = int(month)
        day              = int(day)
        subscribe_start  = datetime.datetime(year, month, day)
        subscribe_end    = datetime.datetime(year, month, day) + datetime.timedelta(days=30)

        if "product_list" not in data:
            subscribe = Subscription.objects.create(
                user=user,
                size=size,
                food_day_count=food_day_count,
                food_week_count=food_week_count,
                food_period=food_period,
                food_start=subscribe_start,
                food_end=subscribe_end,
            )

            food_count = food_day_count * food_week_count * food_period

            product_list = []
            for i in range(0, food_count):
                number = random.randint(1, 71)
                while number in product_list:
                    number = random.randint(1, 71)
                product_list.append(number)

            for product_id in product_list:
                SubscriptionProduct.objects.create(
                    subscription=subscribe,
                    product=Product.objects.get(id=product_id)
                )
        elif "product_list" in data:
            subscribe = Subscription.objects.create(
                user=user,
                size=size,
                food_day_count=food_day_count,
                food_week_count=food_week_count,
                food_period=food_period,
                food_start=subscribe_start,
                food_end=subscribe_end,
            )
            for product_id in product_list:
                SubscriptionProduct.objects.create(
                    subscription=subscribe,
                    product=Product.objects.get(id=product_id)
                )

        return JsonResponse({
            "message" : "SUCCESS",
        })

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
