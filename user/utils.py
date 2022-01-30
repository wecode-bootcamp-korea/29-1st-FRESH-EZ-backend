from django.http import JsonResponse

import jwt

from my_settings import JWT_SECRET_KEY, ALGORITHM
from user.models import User


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            payload = request.headers.get('Authorization')
            _, token = payload.split(" ")
            payload      = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id=payload['id'])
            request.user = user
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN' }, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)
        return func(self, request, *args, **kwargs)
    return wrapper