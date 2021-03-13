from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.template.loader import render_to_string
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order,OrderItem
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from django.conf import settings
from django.http import HttpResponse

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

@staff_member_required
def admin_order_pdf(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    html=render_to_string('admin/orders/order/pdf.html',{
        'order':order})
    response=HttpResponse(content_type='application/pdf')
    response['Content-Dispositon']='attachment; filename="order_{}.pdf"'.format(order.id)
    css=weasyprint.CSS(settings.STATIC_ROOT+'css/pdf.css')
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[css])
    return response

    



    

