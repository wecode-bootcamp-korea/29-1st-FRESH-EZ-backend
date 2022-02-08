import json
from datetime import datetime, timedelta
import random
import jwt

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.views import View
from django.conf import settings
from product.models import Product, Category, Option, Cart
from subscription.models import Subscription, SubscriptionProduct
from user.models import User

class ProductListView(View):
    def get(self, request):
        category_id     = request.GET.get('categoryId', None)
        purchase_method = request.GET.get('method', None)
        offset          = request.GET.get('offset', 0)
        limit           = request.GET.get('limit', 100)

        filter_set = {}
        
        if category_id:
            filter_set["category_id"] = int(category_id)

        if purchase_method:
            filter_set["purchasemethod_set"] = purchase_method
        
        products = Product.objects.filter(**filter_set).select_related('category')\
            .prefetch_related('productimage_set')[offset:offset+limit]

        results = [
            {
                'name'       : product.name,
                'category'   : product.category.pk,
                'price'      : product.price,
                'small_desc' : product.small_desc,
                'image'      : product.productimage_set.first().image_url,
                'allergy_id' : product.allergy_id,
            } for product in products
        ]

        return JsonResponse({'products_list': products_list}, status=201)

class SubscribeOptionView(View):
    @login_reqiured
    def post(self, request):
        data                 = json.loads(request.body)
        user                 = request.user
        category_id          = int(data['category_id'])
        product_ids          = data["product_ids"] # [10,51,110] or []
        subscription_size_id = data['size']
        food_day_count       = int(data['food_day_count'])
        food_week_count      = int(data['food_week_count'])
        food_period          = int(data['food_period'])
        start_date           = datetime.strptime(data["food_start_date"], "%Y-%m-%d")
        end_date             = start_date + timedelta(days=30)
        food_count           = food_day_count * food_week_count * food_period
        food_list_length     = food_count
        MAX_COUNT            = 5

        subscription = Subscription.objects.create(
            user            = user,
            size_id         = size_id,
            food_day_count  = food_day_count,
            food_week_count = food_week_count,
            food_period     = food_period,
            food_start      = subscribe_start,
            food_end        = subscribe_end,
        )

        if not product_ids:

            cycle_count = food_count // MAX_COUNT

            if food_count % MAX_COUNT != 0:
                cycle_count += 1

            for i in range(0, cycle_count):
                if food_count >= 5:
                    products += Product.objects.filter(category=category_id)[:5]
                    food_count -= 5
                elif food_count < 5:
                    products += Product.objects.filter(category=category_id)[:food_count]
                    food_count = 0

        for product in products:
            SubscriptionProduct.objects.create(
                subscription=subscribe,
                product=Product.objects.get(id=product.id)
            )
        
        return JsonResponse({"message" : "SUCCESS", "food_length" : food_list_length})


class SubscribeTotalPriceView(View):
    def post(self, request):
        data = json.loads(request.body)

        category_id = int(data['category_id'])
        food_day_count = int(data['food_day_count'])
        food_week_count = int(data['food_week_count'])
        food_period = int(data['food_period'])

        food_count = food_day_count * food_week_count * food_period
        food_length = food_count

        cycle_count = food_count // 5

        if food_count % 5 != 0:
            cycle_count += 1

        product_instance_list = []
        for i in range(0, cycle_count):
            if food_count >= 5:
                product_instance_list += Product.objects.filter(category=category_id)[:5]
                food_count -= 5
            elif food_count < 5:
                product_instance_list += Product.objects.filter(category=category_id)[:food_count]
                food_count = 0

        total_price = 0
        for product in product_instance_list:
            total_price += product.price

        return JsonResponse({
            "message": "SUCCESS",
            "food_count": food_length,
            "total_price": total_price,
        })

class ProductDetailView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        productimage = product.productimage_set.all()
        title_image_url = productimage[0].image_url
        str_title_image_url = str(title_image_url)

        allergy_list = [product_allergy.allergy.name for product_allergy in product.productallergy_set.all()]

        return JsonResponse({
            "message" : "SUCCESS",
            "name" : product.name,
            "category" : product.category.name,
            "price" : product.price,
            "desc" : product.desc,
            "small_desc" : product.small_desc,
            "allergy" : allergy_list,
            "title_image_url" : str_title_image_url,
        }, status=200)

class SubscribeDetailView(View):
    def get(self, request, category_id):
        """
        products = [
            {
                "name",
                "url",
                "price"
            },
            {
                "name",
                "url",
                "price"
            },
            {
                "name",
                "url",
                "price"
            },
        ]
        """
        category = Category.objects.get(id=category_id)
        product_instance_list = Product.objects.filter(category=category.id)
        product_name_list = []
        product_image_list = []
        product_price_list = []

        for product in product_instance_list:
            product_name_list.append(product.name)

            productimage = product.productimage_set.all()
            title_image_url = productimage[0].image_url
            str_title_image_url = str(title_image_url)
            product_image_list.append(str_title_image_url)

            product_price_list.append(product.price)

        return JsonResponse({
            "message": "SUCCESS",
            "products" : product_name_list,
            "image_list" : product_image_list,
            "price": product_price_list,
        }, status=200)
