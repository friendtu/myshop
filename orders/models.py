from django.db import models
from shop.models import Product

# Create your models here.

class Order(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    email=models.EmailField()
    address=models.CharField(max_length=250)
    postal_code=models.CharField(max_length=10)
    city=models.CharField(max_length=50)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    paid=models.BooleanField(default=False)
    braintree_id=models.CharField(max_length=150,blank=True)

    class Meta:
        ordering=['-created']

    def __str__(self):
        return sum(item.get_cost() for item in self.items)
        

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="order_items")
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price*self.quantity






