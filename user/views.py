import json

import bcrypt
import jwt
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.conf import settings


from .models import User, Allergy, UserAllergy
from .utils import login_decorator
from .validator import UserEmailvalidationRule, UserPasswordvalidationRule, \
    UserValidationRule, UserValidation


class SignUpView(View):
    def post(self,request):
        try:
            data        = json.loads(request.body)
            name        = data['name']
            email       = data['email']
            password    = data['password']
            nickname    = data['nickname']
            phone       = data['phone']
            birth       = data['birth']
            sex         = data['sex']
            allergy_ids = data['allergy_ids']

            rules = [
                UserEmailvalidationRule("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
                UserPasswordvalidationRule("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}"),
            ]

            validation = UserValidation(rules)
            validation.validate(data)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            user = User.objects.create(
                name     = name,
                email    = email,
                password = hashed_password,
                nickname = nickname,
                phone    = phone,
                birth    = birth,
                sex      = sex,
            )

            if allergy_ids:
                UserAllergy.objects.bulk_create([UserAllergy(
                    allergy_id=allergy_id,
                    user_id=user.id
                ) for allergy_id in allergy_ids])

            return JsonResponse({'message' :'SUCCESS'}, status = 201 )

        except KeyError:
            return JsonResponse({'message' : 'KEYERROR'}, status = 400)

        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status = 400)

        except IntegrityError:
            return JsonResponse({'message' : 'Duplicate_Email'}, status = 400)


class AllergyListView(View):
    def get(self, request):

        allergies = Allergy.objects.all()
        results = [{
            'allergy_name': allergy.name,
            'allergy_id': allergy.pk,
        } for allergy in allergies]

        return JsonResponse({'allergies_list' : results}, status= 200)

class SignInView(View):
    def post(self,request):
        try:

            data = json.loads(request.body)

            email = data['email']
            password = data['password']

            rules = [
                UserEmailvalidationRule("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
                UserPasswordvalidationRule("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}"),
            ]

            validation = UserValidation(rules)
            validation.validate(data)


            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message": "INVALID_USER (password)"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER (email)"}, status=401)

        access_token = jwt.encode({'id': user.id}, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

        return JsonResponse({"message" : "SUCCESS", "JWT" : access_token}, status=200)

class UserAllergyView(View):
    @login_decorator
    def get(self, request):
        user_allergies = [{
            "id"   : user_allergy.id,
            "name" : user_allergy.name
        } for user_allergy in request.user.allergies.all()]

        return JsonResponse({'user_allergies': user_allergies}, status=200)

class EmailDupValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']

            if User.objects.get(email=email):
                return JsonResponse({"message": "Duplicate (email)"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"message": "SUCCESS"}, status=200)