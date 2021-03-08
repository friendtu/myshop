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
        #client_token=braintree.

        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.Sandbox,
                merchant_id="c8ysmy3956rnqhms",
                public_key="b74vs7gkt33gsxyf",
                private_key="3d6098d7bc6611fcfea8303799338716s"
            )
        )
        client_token = gateway.client_token.generate()

        return render(request,'payment/process.html',{
                            'order':order,
                            'client_token':client_token
                    })

def payment_done(request):
    pass

def payment_canceled(request):
    pass


