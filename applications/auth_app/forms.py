from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)
        field_classes = {"email": forms.EmailField}
