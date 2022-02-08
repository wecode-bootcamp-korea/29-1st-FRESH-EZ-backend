class UserValidationRule:
    def validate(self, user):
        return all(getattr(self, 'validate_' + key)(user) for key in self.__dict__.keys())

class UserNamevalidationRule(UserValidationRule):
    def __init__(self, max_length, min_length):
        self.max_length = max_length
        self.min_length = min_length

    def validate_min_length(self, user):
        return len(user["name"]) > self.min_length
    
    def validate_max_length(self, user):
        return len(user["name"]) < self.max_length
   
class PhoneNumberValidationRule(UserValidationRule):
    def __init__(self, phone_number_regex):
        self.phone_number_regex = phone_number_regex

    def validate_phone_number_regex(self, user):
        return re.match(self.phone_number_regex, user.phone_number 
 
class UserValidation:
    def __init__(self, rules):
        self.rules = rules

    def validate(self, user):
        return all(rule.validate(user) for rule in self.rules)


# signup views.py
user  = {"name" : "홍홍홍", "phone_number" : "010-7402-0990"}
rules = [
    UserNamevalidationRule(max_length = 10, min_length = 5), 
    PasswordValidationRule(),
    BirthDateValidationRule(),
    PhoneNumberValidationRule('aa')
]

validation = UserValidationRule(rules)
validation.validate(user)

# signin views.py
user  = {"name" : "홍홍홍", "password" : "xxxxxxx"}
rules = [
    UserNamevalidationRule(max_length = 100, min_length = 500), 
    PhoneNumberValidationRule('111')
    PasswordValidationRule(),
]

validation = UserValidationRule(rules)
validation.validate(user)
