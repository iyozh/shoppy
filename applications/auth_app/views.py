from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from applications.auth_app.forms import RegistrationForm, CodeForm
from applications.auth_app.models import User
from applications.auth_app.utils import generate_code
from project.tasks import send_email_confirmation


class SignInView(LoginView):
    template_name = "auth_app/sign-in.html"


class CustomLogoutView(LogoutView):
    template_name = "auth_app/logout.html"


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            message_code = generate_code()
            user = authenticate(email=email, password=raw_password)
            user.code = message_code
            user.save()
            send_email_confirmation.delay(email, message_code)
            if user and user.is_confirmed:
                login(request, user)
                return redirect('showcase:home')
            else:
                form = CodeForm()
                return redirect('auth_app:confirm-page')
    else:
        form = RegistrationForm()
    return render(request, 'auth_app/sign-up.html', {'form': form})

def confirm_account(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            user = User.objects.get(code=code)
            if user:
                user.is_confirmed = True
                user.save()
                login(request, user)
                return redirect('showcase:home')
    form = CodeForm()
    return render(request, 'auth_app/confirm.html', {'form': form})