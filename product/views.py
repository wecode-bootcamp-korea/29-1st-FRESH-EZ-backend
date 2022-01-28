import json
import datetime

from django.http import JsonResponse

from django.views import View

from product.models import Product
from subscription.models import Subscription
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

        year, month, day = food_start.split("-")
        year             = int(year)
        month            = int(month)
        day              = int(day)
        subscribe_start  = datetime.datetime(year, month, day)
        subscribe_end    = datetime.datetime(year, month, day) + datetime.timedelta(days=30)
        product          = Product.objects.get(id=1)

        subscribe = Subscription.objects.create(
            user=user,
            size=size,
            food_day_count=food_day_count,
            food_week_count=food_week_count,
            food_period=food_period,
            food_start=subscribe_start,
            food_end=subscribe_end,
            product=product
        )

        print(subscribe)

        return JsonResponse({
            "message" : "SUCCESS",
        }, status=200)
