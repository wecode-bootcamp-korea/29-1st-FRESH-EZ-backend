import json

import bcrypt
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.views import View

from .models import User, Allergy, UserAllergy
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

