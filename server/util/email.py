from flask_mail import Message
from flask import current_app
from typing import List
import os

def send_email(recipients: List[str], subject: str, template: str):
    """
    This function sends an email to the recipient email address list.

    :param recipients: the email addresses to send to as a list
    :param subject: The subject of the email.
    :param template: The template html to use in the email.
    """
    sender = f"{os.getlogin()}@dcs.warwick.ac.uk"
    message = Message(
        sender=("ACS", sender),
        subject=subject,
        recipients=recipients,
        html=template,
    )

    current_app.mail.send(message)


