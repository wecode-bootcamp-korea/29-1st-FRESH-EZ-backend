from django.urls import path

from product.views import DetailView

urlpatterns = [
    path('/detail/<int:pk>', DetailView.as_view()),
]