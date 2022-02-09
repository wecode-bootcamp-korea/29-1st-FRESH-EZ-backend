from django.http import JsonResponse

import jwt

from django.conf import settings
from user.models import User


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            payload = request.headers.get('Authorization')
            payload      = jwt.decode(payload, settings.JWT_SECRET_KEY, settings.ALGORITHM)
            user         = User.objects.get(id=payload['id'])
            request.user = user
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN' }, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)
        return func(self, request, *args, **kwargs)
    return wrapper
