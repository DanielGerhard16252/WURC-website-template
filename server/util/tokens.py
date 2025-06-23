# project/token.py

from itsdangerous import URLSafeTimedSerializer

from flask import current_app
from datetime import datetime

# https://realpython.com/handling-email-confirmation-in-flask/#add-email-confirmation was used to help

reset_token_delimiter = "$"
def generate_reset_token(email: str):
    """
    This function generates a password reset token to be sent to the email address. It also concats
    the email with the current date and time so that it is different from just the email confirmation token.

    :param email: the email being encoded
    :returns: result of serializer.dumps
    """
    serializer = URLSafeTimedSerializer(current_app.security_key)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # get the time to seconds
    return serializer.dumps(f"{email}{reset_token_delimiter}{now}", salt=current_app.security_salt)

def confirm_reset_token(token, expiration=900):
    """
    This function checks a password reset token.

    :param token: the token being checked
    :param expiration: the time until the token expires - default 15 mins.
    :returns: False if the token is expired, otherwise the email
    """
    serializer = URLSafeTimedSerializer(current_app.security_key)
    try:
        email = serializer.loads(
            token,
            salt=current_app.security_salt,
            max_age=expiration
        ).split(reset_token_delimiter)[0]
    except:
        return False
    
    return True