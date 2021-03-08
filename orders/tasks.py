from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from time import sleep
from myshop.celery import app as celery_app

@celery_app.task
def order_created(order_id):
    order=Order.objects.filter(id=order_id)
    subject='Order number {}'.format(order.id)
    message='Dear {},\n\nYou have successfully placed an order.\
            Your order is is {}.'.format(order.first_name,order.id)
    mail_sent=send_mail(subject,message,'admin@myshop.com',[order.email])

    return mail_sent