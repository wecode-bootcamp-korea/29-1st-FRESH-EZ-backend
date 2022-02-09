import re

from django.core.exceptions import ValidationError

from .models import User

class UserValidationRule:
    def validate(self, user):
        return all(getattr(self, 'validate_' + key)(user) for key in self.__dict__.keys())

class UserEmailvalidationRule(UserValidationRule):
    def __init__(self, email):
        self.email = email

    def validate_email(self, user):

        return re.match(self.email, user['email'])

class UserPasswordvalidationRule(UserValidationRule):
    def __init__(self, password):
        self.password= password

    def validate_password(self, user):
        return re.match(self.password , user["password"])

class UserValidation:
    def __init__(self, rules):
        self.rules = rules

    def validate(self, user):
        if all(rule.validate(user) for rule in self.rules):
            return True
        else:
            raise ValidationError("ValidationError")


