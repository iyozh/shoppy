from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Count
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from applications.auth_app.models import User
from applications.showcase.models import Product
from project.celery import app
from applications.orders.models import Order, OrderItem


@app.task
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


@app.task
def hello():
    print("Hello there!")


@app.task
def reindex_product(product_id):
    from applications.showcase.models import Product

    product = Product.objects.get(id=product_id)
    product.add_index_to_es()


@app.task
def send_order_notification(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Заказ № {}'.format(order_id)
    message = f'Уважаемый(ая) {order.first_name}, вы успешно сделали заказ.\'' \
              f'Ваш заказ - под номером {order.id}'

    send_mail(subject,
              message,
              "shoppyofficial22@gmail.com",
              [order.email])


@shared_task
def send_popular_products_list():
    orders = OrderItem.objects.select_related('product').values('product_id', 'product__name', 'product__price',
                                                                'product__description').annotate(
        total_orders=Count('id')).order_by('-total_orders')
    popular_product = orders[0]

    message_subject = "Популярные товары за последнюю неделю"
    html_message = render_to_string('auth_app/popular_list.html', {'popular_product': popular_product})

    emails = User.objects.filter(is_confirmed=True).values('email')
    emails = [dct['email'] for dct in emails]

    plain_message = strip_tags(html_message)
    send_mail(message_subject,
              plain_message,
              "shoppyofficial22@gmail.com",
              [*emails],
              fail_silently=False,
              html_message=html_message)
