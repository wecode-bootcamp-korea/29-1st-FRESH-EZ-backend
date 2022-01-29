from django.urls import path

from product.views import SubscribeDetailView, ProductDetailView

urlpatterns = [
    path('/detail/<int:pk>', ProductDetailView.as_view()),
    path('/subscribe-detail/<int:category_id>', SubscribeDetailView.as_view()),
]