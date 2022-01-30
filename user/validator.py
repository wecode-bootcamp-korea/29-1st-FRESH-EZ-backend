import re

from django.core.exceptions import ValidationError

from user.models import User


def validate_email(email):
    if not re.match("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise ValidationError("ERROR : INVALID_VALUE (email)")

def validate_password(password):
    if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}", password):
        raise ValidationError("ERROR : INVALID_VALUE (password)")

def validate_email_duplicate(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError("ERROR : EMAIL_DUPLICATE")