from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator
import os


def send_email_for_verify(request, user):
    current_site = request.get_host()
    context = {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    }
    message = render_to_string('users/mails/verify_email.html', context=context,)
    email = EmailMessage('Завершение регистрации на сайте Skystore', message, to=[user.email],)

    email.send()


def send_email_for_reset(request, email, new_password):
    current_site = request.get_host()

    context = {
        'domain': current_site,
        'new_password': new_password
    }

    message = render_to_string('users/mails/password_reset_email.html', context=context,)
    email = EmailMessage('Восстановление пароля на сайте Skystore', message, to=[email])

    email.send()