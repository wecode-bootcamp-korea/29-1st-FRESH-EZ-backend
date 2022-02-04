import json, bcrypt, jwt

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View

from user.models import User, Allergy, UserAllergy
from user.validator import validate_email, validate_password, validate_email_duplicate
from my_settings import JWT_SECRET_KEY, ALGORITHM

class AllergyInfoView(View):
    def get(self, request):
        allergies = Allergy.objects.all()
        allergies_list = []

        for allergy in allergies:
            allergies_dic = {
                'allergy_name': allergy.name,
                'allergy_id' : allergy.pk,
            }
            allergies_list.append(allergies_dic)

        return JsonResponse({'allergies_list' : allergies_list}, status= 201)

class UserAllergyView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            jwt_token = data['jwt_token'].encode()
            jwt_decoded = jwt.decode(jwt_token, JWT_SECRET_KEY, ALGORITHM)
            user_id = jwt_decoded['id']

            user_allergies = UserAllergy.objects.filter(user_id=user_id)

            user_allergies_list = []

            for user_allergy in user_allergies:
                user_allergies_list.append(user_allergy.allergy.pk)

            return JsonResponse({'user_allergies': user_allergies_list}, status=201)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=401)
        except UserAllergy.DoesNotExist:
            return JsonResponse({'message': 'NO_DATA'}, status=401)
        except jwt.InvalidSignatureError:
            return JsonResponse({'message': 'InvalidSignatureError'}, status=401)

class SignUpView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            name     = data['name']
            email    = data['email']
            password = data['password']
            nickname = data['nickname']
            phone    = data['phone']
            birth    = data['birth']
            sex      = data['sex']

            validate_email(email)
            validate_password(password)
            validate_email_duplicate(email)

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

            user_allergy_list =[]

            if 'allergy_id' in data:
                for allergy_id in data['allergy_id']:
                    user_allergy_list.append(UserAllergy(allergy_id=allergy_id,user_id=user.pk))
                UserAllergy.objects.bulk_create(user_allergy_list)

            return JsonResponse({'message' :'SUCCESS'}, status = 201 )
        except KeyError:
            return JsonResponse({'message' : 'KEYERROR'}, status = 400)
        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status = 400)

class SignInView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            email = data['email']
            password = data['password']
            user = User.objects.get(email=email)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER (email)"}, status=401)

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return JsonResponse({"message" : "INVALID_USER (password)"}, status=401)

        access_token = jwt.encode({'id': user.id},JWT_SECRET_KEY,algorithm=ALGORITHM)

        return JsonResponse({"message" : "SUCCESS", "JWT" : access_token}, status=200)