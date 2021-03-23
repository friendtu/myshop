from django.shortcuts import render,get_object_or_404,redirect
import braintree
from orders.models import Order
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import weasyprint
from django.conf import settings
from shop.recommender import Recommender

# Create your views here.



def payment_process(request):
    order_id=request.session['order_id']
    order=get_object_or_404(Order,id=order_id)

    if request.method=='POST':
        nonce=request.POST.get('payment_method_nonce',None)
        result=braintree.Transaction.sale({
            'amount':'{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce':nonce,
            "options": {
                "submit_for_settlement": True
            }
        })
        if result.is_success:
            order.paid=True
            order.braintree_id=result.transaction.id
            order.save()

            #record products to be bought together
            r=Recommender()
            products=[item.product for item in order.items.all()]
            r.products_bought(products)

            #create mail of invoice
            subject="My shop - invoice no. {}".format(order.id)
            message='Please, find attateched the invoice for your recent purchases.'
            email=EmailMessage(subject,message,'admin@myshop.com',[order.email])

            html=render_to_string('admin/orders/order/pdf.html',{
                    'order':order
                })
            stylesheets=[weasyprint.CSS(settings.STATIC_ROOT+'css/pdf.css')]
            out=weasyprint.HTML(string=html).write_pdf(stylesheets=stylesheets)

            email.attach('order_{}'.format(order.id),out,'application/pdf')
            email.send()

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')

    else:
        #client_token=braintree.ClientToken.generate()
      
        gateway = braintree.BraintreeGateway(
            braintree.Configuration.instantiate()
        )
        client_token = gateway.client_token.generate()
        
        return render(request,'payment/process.html',{
                            'order':order,
                            'client_token':client_token
                    })

def payment_done(request):
    return render(request,'payment/done.html')

def payment_canceled(request):
    return render(request,'payment/canceled.html')


