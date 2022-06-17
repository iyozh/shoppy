from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from applications.auth_app.forms import RegistrationForm, ConfirmationTokenForm
from applications.auth_app.models import User
from applications.auth_app.utils import encode_verification_code, decode_verification_code
from project.tasks import send_email_confirmation


class SignIn(LoginView):
    template_name = 'auth_app/sign-in.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            email = form.cleaned_data.get('username')
            user = User.objects.get(email=email)

            if user.is_confirmed:
                return super().form_valid(form)
            else:
                error = "Account hasn't been confirmed"
                return render(request, 'auth_app/sign-in.html', {'errors': error, 'form': form})
        return render(request, 'auth_app/sign-in.html', {'form': form})


class CustomLogoutView(LogoutView):
    template_name = "auth_app/logout.html"


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(email=email, password=raw_password)
            confirmation_token = encode_verification_code(user, 1)
            user.code = confirmation_token
            user.save()

            confirmation_link = f'http://localhost:8000/auth/confirm?token={confirmation_token}'
            send_email_confirmation.delay(email, confirmation_link)

            if user and user.is_confirmed:
                login(request, user)
                return redirect('showcase:home')
            else:
                return render(request, 'auth_app/confirm.html', {'email': email})
    else:
        form = RegistrationForm()
    return render(request, 'auth_app/sign-up.html', {'form': form})

def confirm_account(request):
    token = request.GET.get('token')
    form = ConfirmationTokenForm({'token': token})

    if form.is_valid():
        token_data = decode_verification_code(token)
    else:
        raise ValidationError('Incorrect data')

    email = token_data.get('email')
    user = User.objects.get(email=email)

    if not user.is_confirmed:
        user.is_confirmed = True
        user.save()

        return render(request, 'auth_app/confirm.html', {'is_confirmed': True})
    else:
        return render(request, 'auth_app/confirm.html', {'msg': 'Account has already confirmed'})