from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from shop.models import Product
from django.shortcuts import get_object_or_404
from .forms import CartAddProductForm

# Create your views here.

def cart_detail(request):
    cart=Cart(request)
    return render(request,'cart/detail.html',{
        'cart':cart,
    })

@require_POST
def cart_add(request, product_id):
    cart=Cart(request)
    product=get_object_or_404(Product,id=product_id)
    form=CartAddProductForm(request.POST)
    if form.is_valid():
        cd=form.cleaned_data
        cart.add(product=product,quantity=cd["quantity"],update_quantity=cd["update"])
        return redirect('cart:cart_detail')
        
def cart_remove(request,product_id):
    cart=Cart(request)
    product=get_object_or_404(Product,id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
