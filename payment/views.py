from django.shortcuts import render,get_object_or_404
import braintree
from orders.models import Order
# Create your views here.



def payment_process(request):
    order_id=request.session['order_id']
    order=get_object_or_404(Order,id=order_id)

    if request.method=='POST':
        pass
    else:
        #client_token=braintree.ClientToken.generate()
        return render(request,'payment/process.html',{
                            'order':order,
                    })

def payment_done(request):
    pass

def payment_canceled(request):
    pass


