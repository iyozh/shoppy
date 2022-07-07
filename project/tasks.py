from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import task

@shared_task
def send_email_confirmation(email, link):
    message_subject = "Пожалуйста, подтвердите свой аккаунт."
    html_message = render_to_string('auth_app/mail.html', {'link': link})
    plain_message = strip_tags(html_message)
    send_mail(message_subject,
              plain_message,
              "shoppyofficial22@gmail.com",
              [email],
              fail_silently=False,
              html_message=html_message)

@shared_task
def hello():
    print("Hello there!")

@shared_task
def reindex_product(product_id):
    from applications.showcase.models import Product

    product = Product.objects.get(id=product_id)
    product.add_index_to_es()
