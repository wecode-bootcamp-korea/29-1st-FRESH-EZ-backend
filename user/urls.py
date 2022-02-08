from django.urls import path

from user.views import AllergyListView,SignUpView

urlpatterns = [
    path('/allergy', AllergyListView.as_view()),
    path('/signup', SignUpView.as_view()),
]