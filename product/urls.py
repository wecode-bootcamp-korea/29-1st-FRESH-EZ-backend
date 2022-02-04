from django.urls import path, include

from product.views import SubscribeDetailView, ProductDetailView, SubscribeOptionView, CartList, CartAdd, CartDelete, ProductListView

urlpatterns = [
    path('/subscribe-option', SubscribeOptionView.as_view()),
    path('/product-detail/<int:product_id>', ProductDetailView.as_view()),
    path('/subscribe-detail/<int:category_id>', SubscribeDetailView.as_view()),
    path('/cart-list', CartList.as_view()),
    path('/cart-add', CartAdd.as_view()),
    path('/cart-delete', CartDelete.as_view()),
    path('/menu', ProductListView.as_view())
]