from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import Form

from applications.auth_app.utils import decode_verification_code


class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)
        field_classes = {"email": forms.EmailField}

def user_token_expired_check(token):
        token_data = decode_verification_code(token)
        expire_at = datetime.strptime(token_data.get('expire_at'), '%Y-%m-%d %H:%M:%S')
        current_time = datetime.utcnow()

        message = "Срок действия токена истек. Запросите новое письмо"
        if expire_at < current_time:
            raise ValidationError(message)

        return token_data


class ConfirmationTokenForm(Form):

    token = forms.CharField(validators=[
        user_token_expired_check
    ])

