from django.shortcuts import render
from django.views.decorators.http import require_POST
from .cart import Cart

# Create your views here.

def cart_detail(request):
    cart=Cart(request)
    return render(request,'cart/detail.html',{
        'cart':cart,
    })

@require_POST
def cart_add(request, product_id):
    pass

def cart_remove(request,product_id):
    pass
