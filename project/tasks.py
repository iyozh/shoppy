from celery import shared_task
from django.core.mail import send_mail

from project.celery import app


@shared_task
def send_email_confirmation(email, message):
    send_mail('Вы успешно зарегистрировались.',
              f'Подтвердите своей аккаунт, используя этот код: {message}',
              'shoppyofficial22@gmail.com',
              [email],
              fail_silently=False)

@shared_task
def hello():
    print("Hello there!")