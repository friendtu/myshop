from django.shortcuts import render,get_object_or_404,redirect
import braintree
from orders.models import Order

# Create your views here.



def payment_process(request):
    order_id=request.session['order_id']
    order=get_object_or_404(Order,id=order_id)

    if request.method=='POST':
        nonce=request.POST.get('payment_method_nonce',None)
        result=braintree.Transactoin.sale({
            'amount':order.get_total_cost(),
            'payment_method_nonce':nonce,
            "options": {
                "submit_for_settlement": True
            }
        })
        if result.is_success:
            order.paid=True
            order.braintree_id=result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')

    else:
        client_token=braintree.ClientToken.generate()
        #client_token="sandbox_ktdjydgb_c8ysmy3956rnqhms"

        '''
        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.Sandbox,
                merchant_id="c8ysmy3956rnqhms",
                public_key="b74vs7gkt33gsxyf",
                private_key="3d6098d7bc6611fcfea8303799338716"
            )
        )
        client_token = gateway.client_token.generate()
        '''
        
        return render(request,'payment/process.html',{
                            'order':order,
                            'client_token':client_token
                    })

def payment_done(request):
    return render(request,'payment/done.html')

def payment_canceled(request):
    return render(request,'payment/canceled')


