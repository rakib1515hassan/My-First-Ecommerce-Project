from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_email(email, email_token):
    subject = "Your account needs to be verified"
    message = f"Click on the link to verify http://127.0.0.1:8000/activate_email/{email_token}"
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)

def send_otp(email, otp):
    subject = "Your account needs to be verified"
    message = f"Your OTP Code:" +str(otp)
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)