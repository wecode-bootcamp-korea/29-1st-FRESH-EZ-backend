from django.urls import path

from user.views import AllergyListView, SignUpView, SignInView, UserAllergyView, EmailDupValidationView

urlpatterns = [
    path('/allergy', AllergyListView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/allergies', UserAllergyView.as_view()),
    path('/duplication', EmailDupValidationView.as_view())
]
