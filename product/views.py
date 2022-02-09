import json
from datetime import datetime
from datetime import timedelta

import jwt
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views import View



from product.models import Product, Category, Cart, ProductAllergy, ProductImage, Option
from subscription.models import Subscription, SubscriptionProduct
from user.models import User
from user.utils import login_decorator



class ProductListView(View):
    def get(self, request):
        category_id     = request.GET.get('categoryId', None)
        offset          = int(request.GET.get('offset', 0))
        limit           = int(request.GET.get('limit', 100))

        filter_set = {}

        if category_id:
            filter_set["category"] = int(category_id)


        products = Product.objects.filter(**filter_set).select_related('category')\
            .prefetch_related('productimage_set').prefetch_related('productallergy_set')[offset:offset+limit]

        results = [
            {
                'name'       : product.name,
                'category'   : product.category.pk,
                'price'      : product.price,
                'small_desc' : product.small_desc,
                'image'      : str(product.productimage_set.first().image_url),
                'allergy_id' : product.productallergy_set.first().allergy.pk,
            } for product in products
        ]

        return JsonResponse({'products_list': results}, status=201)

class FilteredProductListView(View):
    @login_decorator
    def post(self,request):
        try:
            user = request.user

            category_id = request.GET.get('categoryId', None)
            offset = int(request.GET.get('offset', 0))
            limit = int(request.GET.get('limit', 100))

            filter_set = {}

            if category_id:
                filter_set["category_id"] = int(category_id)

            user_allergies = user.userallergy_set.all()
            allergies = [user_allergy.allergy.pk for user_allergy in user_allergies]

            filltered_products = Product.objects.filter(~Q(productallergy__allergy__in=allergies) & Q(**filter_set))\
            .select_related('category').prefetch_related('productimage_set').prefetch_related('productallergy_set')[offset:offset+limit]

            products_filtered = [
                {
                    'name'               : filtered_product.name,
                    'product_id'         : filtered_product.pk,
                    'category'           : filtered_product.category.pk,
                    'price'              : filtered_product.price,
                    'small_desc'         : filtered_product.small_desc,
                    'allergy_id'         : filtered_product.productallergy_set.first().allergy.pk,
                    'image'              : str(filtered_product.productimage_set.first().image_url),
                } for filtered_product in filltered_products
            ]

            return JsonResponse({'products_filtered':products_filtered}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=401)

class SubscribeOptionView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        category_id = int(data['categoryId'])
        subscription_size_id = data['size']
        food_day_count = int(data['food_day_count'])
        food_week_count = int(data['food_week_count'])
        food_period = int(data['food_period'])
        start_date = datetime.strptime(data["food_start_date"], "%Y-%m-%d")
        end_date = start_date + timedelta(days=30)
        food_count = food_day_count * food_week_count * food_period
        food_list_length = food_count
        MAX_COUNT = 5

        product_ids = 0
        if 'product_ids' in data:
            product_ids = data["product_ids"]

        option = Option.objects.get(id=subscription_size_id)

        subscribe = Subscription.objects.create(
            user=user,
            size=option,
            food_day_count=food_day_count,
            food_week_count=food_week_count,
            food_period=food_period,
            food_start=start_date,
            food_end=end_date,
        )

        if not product_ids:
            cycle_count = food_count // MAX_COUNT

            if food_count % MAX_COUNT != 0:
                cycle_count += 1

            products = []
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
                product=Product.objects.get(id=product.pk)
            )

        products_list = []

        for product in products:
            products_list.append({
                "name" : product.name,
                "price" : product.price,
            })

        return JsonResponse({
            "message" : "SUCCESS",
            "food_length" : food_list_length,
            "food_list" : products_list,
        })

class SubscribeProductList(View):
    def get(self, request):
        product_dict = dict()
        category_instance_list = Category.objects.all()
        for category in category_instance_list:
            product_instance_list = Product.objects.filter(category=category.pk)
            product_list = list()
            for product in product_instance_list:
                product_list.append(product.price)
            product_dict[category.pk] = product_list

        return JsonResponse({
            "message": "SUCCESS",
            "products": product_dict
        })

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

        product_instance_list = Product.objects.filter(category=category_id)
        product_list = []

        for product in product_instance_list:
            product_dict = {}
            product_dict["name"] = product.name

            productimage = product.productimage_set.all()
            title_image_url = productimage[0].image_url
            str_title_image_url = str(title_image_url)
            product_dict["url"] = str_title_image_url

            product_dict["price"] = product.price

            product_list.append(product_dict)

        return JsonResponse({
            "message": "SUCCESS",
            "product_list": product_list,
        }, status=200)

class CartList(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            # 유저 확인
            # token   = data['jwt']
            email = data['email']

            # payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
            # user    = User.objects.get(id=payload['id'])
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER (email)"}, status=401)

        # 구독 장바구니
        subscription_instance_list = Subscription.objects.filter(user=user)
        subscription_list = []
        for subscription in subscription_instance_list:
            if not subscription.receipt.exists():
                food_instance_list = subscription.subscription_food.all()
                food_list = []
                food_total_price = 0
                for food in food_instance_list:
                    food_list.append({
                        "subscription_food_name": food.product.name,
                        "subscription_food_price": food.product.price,
                    })
                    food_total_price += food.product.price

                subscription_list.append({
                    "id": subscription.id,
                    "user": subscription.user.name,
                    "size": subscription.size.name,
                    "food_day_count": subscription.food_day_count,
                    "food_week_count": subscription.food_week_count,
                    "food_period": subscription.food_period,
                    "food_start": subscription.food_start,
                    "food_end": subscription.food_end,
                    "food_list": food_list,
                    "food_total_price": food_total_price,
                })

        # 단품 장바구니
        cart_instance_list = Cart.objects.filter(user=user)
        cart_list = []
        total_price = 0
        for cart in cart_instance_list:
            cart_list.append({
                "cart_id": cart.id,
                "food_name": cart.product.name,
                "food_price": cart.product.price,
                "food_count": cart.count,
            })
            total_price += cart.product.price

        return JsonResponse({
            "message": "SUCCESS",
            "total_price": total_price,
            "subscription_list": subscription_list,
            "cart_list": cart_list,
        }, status=200)

class CartAdd(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            # 유저 확인
            # token   = data['jwt']
            email = data['email']

            # payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
            # user    = User.objects.get(id=payload['id'])
            user = User.objects.get(email=email)

            # 상품 확인
            product_id = data['product_id']

            product = Product.objects.get(id=product_id)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER (email)"}, status=401)
        except Product.DoesNotExist:
            return JsonResponse({"message": "INVALID_ERROR"}, status=401)

        product_count = int(data['count'])

        cart = Cart.objects.create(
            user=user,
            product=product,
            count=product_count,
        )

        return JsonResponse({
            "message": "SUCCESS",
            "cart_user": cart.user.name,
            "cart_product": cart.product.name,
            "cart_count": cart.count,
        }, status=200)

class CartDelete(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            # 유저 확인
            # token   = data['jwt']
            email = data['email']

            # payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
            # user    = User.objects.get(id=payload['id'])
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER (email)"}, status=401)

        if 'cart_id' in data:
            cart_id = int(data['cart_id'])

            cart_instance_list = Cart.objects.filter(id=cart_id)
            for cart in cart_instance_list:
                cart.delete()

        if 'subscription_id' in data:
            subscription_id = data['subscription_id']

            subscription_instance_list = Subscription.objects.filter(id=subscription_id)
            for subscription in subscription_instance_list:
                subscription.delete()

        return JsonResponse({
            "message": "SUCCESS",
        }, status=200)
