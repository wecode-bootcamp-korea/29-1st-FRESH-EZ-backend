from django.urls import path

from product.views import SubscribeDetailView

urlpatterns = [
    path('/subscribe-detail/<int:category_id>', SubscribeDetailView.as_view()),
]