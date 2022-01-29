from django.urls import path, include

from product.views import SubscribeDetailView, ProductDetailView, SubscribeOptionView

urlpatterns = [
    path('/subscribe-option', SubscribeOptionView.as_view()),
    path('/detail/<int:pk>', ProductDetailView.as_view()),
    path('/subscribe-detail/<int:category_id>', SubscribeDetailView.as_view()),
]