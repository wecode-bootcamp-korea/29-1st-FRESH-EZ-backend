from django.urls import path
from user.views import AllergyInfoView,SignUpView

urlpatterns = [
    path('/allergy', AllergyInfoView.as_view()),
    path('/signup', SignUpView.as_view()),
]