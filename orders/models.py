from django.db import models
from shop.models import Product
from coupans.models import Coupon
from django.core.validators import MinValueValidator,MaxValueValidator
from decimal import Decimal
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Order(models.Model):
    first_name=models.CharField(_('first name'),max_length=30)
    last_name=models.CharField(_('last name'),max_length=30)
    email=models.EmailField(_('e-mail'))
    address=models.CharField(_('address'),max_length=250)
    postal_code=models.CharField(_('postal code'),max_length=10)
    city=models.CharField(_('city'),max_length=50)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    paid=models.BooleanField(default=False)
    braintree_id=models.CharField(max_length=150,blank=True)
    coupon=models.ForeignKey(Coupon,related_name='orders',null=True,on_delete=models.SET_NULL)

    discount=models.IntegerField(default=0,validators=[MaxValueValidator(100),MinValueValidator(0)])

    class Meta:
        ordering=['-created']

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost= sum(item.get_cost() for item in self.items.all())
        return total_cost-total_cost*(self.discount/Decimal('100'))

    def get_discount(self):
        total_cost= sum(item.get_cost() for item in self.items.all())
        return total_cost*(self.discount/Decimal('100'))
        

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="order_items")
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price*self.quantity






