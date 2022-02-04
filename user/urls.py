from django.urls import path

from user.views import AllergyInfoView, SignUpView, SignInView, UserAllergyView

urlpatterns = [
    path('/allergy', AllergyInfoView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/allergies', UserAllergyView.as_view())
]