from django.urls import path, include

from product.views import SubscribeOptionView

urlpatterns = [
    path('/subscribe-option', SubscribeOptionView.as_view()),
]