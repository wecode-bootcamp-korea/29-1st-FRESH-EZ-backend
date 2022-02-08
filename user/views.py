import json, bcrypt, jwt

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View

from user.models import User, Allergy, UserAllergy
from user.validator import validate_email, validate_password, validate_email_duplicate

class AllergyListView(View):
    def get(self, request):
        allergies = Allergy.objects.all()
        results   = [{
            'allergy_name' : allergy.name,
            'allergy_id'   : allergy.pk,
        } for allergy in allergies]

        return JsonResponse({'allergies': results}, status= 200)

class UserAllergyView(View):
    @login_reqiured
    def get(self, request):
        user_allergies = [{
            "id"   : allergy.id,
            "name" : allergy.name
        } for user_allergy in request.user.allergies.all()]

        return JsonResponse({'user_allergies': user_allergies}, status=200)

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

            rules = [UserEmailRule(), UserPasswordRule()]
            user_validator = UserValidation(rules)
            user_validator.validate(user)

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
                    allergy_id = allergy_id,
                    user_id    = user.id
                ) for allergy_id in allergy_ids])

            return JsonResponse({'message' :'SUCCESS'}, status = 201 )

        except KeyError:
            return JsonResponse({'message' : 'KEYERROR'}, status = 400)

        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status = 400)


class SignInView(View):
    def post(self,request):
        data = json.loads(request.body)
        rules = [
            UserNamevalidationRule(max_length = 10, min_length = 5), 
            PasswordValidationRule(),
            BirthDateValidationRule(),
            PhoneNumberValidationRule('aa')
        ]

        try:
            email      = data['email']
            password   = data['password']
            validation = UserValidationRule(rules)
            validation.validate(user)

            user = User.objects.get(email=email)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER (email)"}, status=401)

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return JsonResponse({"message" : "INVALID_USER (password)"}, status=401)

        access_token = jwt.encode({'id': user.id},JWT_SECRET_KEY,algorithm=ALGORITHM)

        return JsonResponse({"message" : "SUCCESS", "JWT" : access_token}, status=200)
