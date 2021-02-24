from django.conf import settings
from shop.models import Product
from decimal import Decimal

class Cart(object):
    session=None
    cart=None

    def __init__ (self,request):
        self.session=request.session
        cart=self.sessoin.get(settings.CART_SESSION_ID)
        if not cart:
            cart=self.session[setting.CART_SESSION_ID]={}
        self.car=cart

    def add(self,product,quantity=1,update_quantity=False):
        product_id=str(product.id)
        if product_id not in self.cart:
            self.cart[product.id]={
                'quanlity':0,
                'price':product.price
            }
        if(update_quantity):
            self.cart[product.id]['quanlity']=quantity
        else:
            self.cart[product.id]['quanlity']+=quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self,product):
        product_id=str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        cart=self.cart.copy()

        for product in products:
            cart[str(product.id)]['product']=product
        
        for item in cart.values():
            item['price']=Decimal(item['price'])
            item['total_price']=item['price']*item['quanlity']
            yield item

    def __len__(self):
        return sum(item['quanlity'] for item in self.cart.values())

    def get_total_price(self):
        return sum( item['quanlity']*item['price'] for item in self.cart.values())
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()


