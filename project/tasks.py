from celery import shared_task
from django.core.mail import send_mail

from project.celery import app


@app.task
def send_email_confirmation(email):
    send_mail('Вы успешно зарегистрировались.',
              'Подтвердите своей аккаунт',
              'shoppyofficial22@gmail.com',
              [email],
              fail_silently=False)

@shared_task
def hello():
    print("Hello there!")