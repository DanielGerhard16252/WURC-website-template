from wtforms.validators import ValidationError
import re
from datetime import datetime, timedelta
from server.util.inputs import is_input_invalid

class InvalidChars(object):
    def __init__(self,  message=None):
        if not message:
            message = f'Invalid characters used in input'
        self.message = message

    def __call__(self, form, field):
        """
        This function checks if an input contains invalid characters, so that
        we can avoid SQL injection attacks.
        """
        try:
            float(field.data)
        except ValueError:
            if is_input_invalid(field.data):
                raise ValidationError(self.message)


class Email(object):
    def __init__(self, message=None):
        if not message:
            message = f'Invalid email address entered'
        
        self.message = message

    def __call__(self, form, field):
        """
        As the standard wtforms email validator requires an additional package not in
        requirements.txt (email_validator), I have made my own here.
        Validates chars (regex) and length.
        """
        # the longest email address possible for any email servers in use is 254 len

        # This regex is checking for alphabetic, period or - characters, then a @, then more of the same from before for a domain (a . is required), then the end of line.
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if len(field.data) > 254 or not re.match(email_regex, field.data):
            raise ValidationError(self.message)
        

class StrongPassword(object):
    def __init__(self, message=None):
        if not message:
            message = f'Password is not strong enough'
        
        self.message = message

    def __call__(self, form, field):
        """
        This function checks if a password is strong enough.
        at least 8 chars, 1 uppercase, 1 lowercse, a number and a symbol
        """
        if len(field.data) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        if not any(char.isupper() for char in field.data):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not any(char.islower() for char in field.data):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not any(char.isdigit() for char in field.data):
            raise ValidationError("Password must contain at least one digit")

        if not any(char in "!@#$%^&()-_=+[]{}|,.<>?`~" for char in field.data):
            raise ValidationError("Password must contain at least one special character")
        

class FutureDate(object):
    def __init__(self, message=None):
        if not message:
            message = f'Date must be in the future and cannot be more than 2 years in the future'
        
        self.message = message

    def __call__(self, form, field):
        """
        This function checks if a date is in the future.
        """
        if not field.data:
            raise ValidationError("No date entered")
        if field.data < datetime.now() or field.data > datetime.now() + timedelta(years=5):
            raise ValidationError(self.message)
        
        
class Postcode(object):
    def __init__(self, message=None):
        if not message:
            message = f'Invalid postcode entered'
        
        self.message = message
    
    def __call__(self, form, field):
        """
        This checks if a postcode is valid.
        """
        text = field.data.upper().replace(' ', '')
        # UK postcode regex from https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Validation
        postcode_regex = r'^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$'
        if not re.match(postcode_regex, text):
            raise ValidationError(self.message)

class ValidExpiryMonth(object):
    def __init__(self, message=None):
        if not message:
            message = f'Invalid expiry month entered'
        
        self.message = message
    
    def __call__(self, form, field):
        """
        This checks if an expiry month is valid (1-12) and if the year is the current year, that the month is not in the past.
        """
        if field.data < 1 or field.data > 12:
            raise ValidationError(self.message)
        
        if form.expiry_year.data == datetime.now().year and field.data < datetime.now().month:
            raise ValidationError(self.message)
        

class ValidCardNumber(object):
    def __init__(self, message=None):
        if not message:
            message = f'Invalid card number entered'
        
        self.message = message
    
    def __call__(self, form, field):
        """
        This checks if a card number is valid. It uses the Luhn algorithm https://www.ibm.com/docs/en/order-management-sw/9.3.0?topic=cpms-handling-credit-cards
        """
        card_number = field.data
        if len(card_number) < 13 or len(card_number) > 19:
            raise ValidationError(self.message)
        
        if not card_number.isdigit():
            raise ValidationError(self.message)
        
        # the card number is reversed and some addition happens - the final total must be divisible by 10
        total = 0
        for i, digit in enumerate(reversed(card_number)):
            if i % 2 == 0:
                total += int(digit)
            else:
                doubled = int(digit) * 2
                if doubled > 9:
                    total += doubled - 9
                else:
                    total += doubled
        
        if total % 10 != 0:
            raise ValidationError(self.message)
        
class ValidCVV(object):
    def __init__(self, message=None):
        if not message:
            message = f'Invalid CVV entered'
        
        self.message = message
    
    def __call__(self, form, field):
        """
        This checks if a CVV is valid. It must be 3 or 4 digits long and only digits
        """
        if len(field.data) < 3 or len(field.data) > 4 or not field.data.isdigit():
            raise ValidationError(self.message)