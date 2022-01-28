from django.urls import path

from product.views import ProductDetailView

urlpatterns = [
    path('/detail/<int:pk>', ProductDetailView.as_view()),
]