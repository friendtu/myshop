from celery import task 
from django.core.mail import send_mail
from .modules import Order

@task
def order_created(order_id):
    sleep(10)
    print('setting mail')