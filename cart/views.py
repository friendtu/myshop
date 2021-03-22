from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from shop.models import Product
from django.shortcuts import get_object_or_404
from .forms import CartAddProductForm
from coupans.forms import CouponApplyForm
from shop.recommender import Recommender

# Create your views here.

def cart_detail(request):
    cart=Cart(request)
    for item in cart:
        item['update_quantity_form']=CartAddProductForm(initial={'quantity':item['quantity'],'update':True})

    coupon_apply_form=CouponApplyForm()
    r=Recommender()
    products=[item['product'] for item in cart]
    recommented_products=r.suggest_products_for(products,max_results=4)

    return render(request,'cart/detail.html',{
        'cart':cart,
        'coupon_apply_form':coupon_apply_form,
        'recommented_products':recommented_products
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
