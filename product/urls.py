from django.urls import path, include

from product.views import SubscribeOptionView
from product.views import ProductDetailView

urlpatterns = [
    path('/subscribe-option', SubscribeOptionView.as_view()),
    path('/detail/<int:pk>', ProductDetailView.as_view()),
]