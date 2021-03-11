from django.shortcuts import render,redirect,reverse,get_object_or_404
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order,OrderItem
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def order_create(request):
    cart=Cart(request)
    if request.method=='POST':
        form=OrderCreateForm(request.POST)
        if form.is_valid():
            order=form.save()
            for item in cart:
                OrderItem.objects.create(order=order,price=item['price'],product=item['product'],quantity=item['quantity'])
            cart.clear()
            #order_created.delay(order.id)
            request.session['order_id']=order.id 
            return redirect(reverse('payment:process'))
            
    else:
        form=OrderCreateForm()
        return render(request,'orders/create.html',
                                {
                                    'form':form,
                                    'cart':cart
                                })


@staff_member_required
def admin_order_detail(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    return render(request,'admin/orders/order/detail.html',{
        'order':order})
    

