from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from applications.auth_app.forms import RegistrationForm
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
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            send_email_confirmation.delay(email)
            return redirect('showcase:home')
    else:
        form = RegistrationForm()
    return render(request, 'auth_app/sign-up.html', {'form': form})
