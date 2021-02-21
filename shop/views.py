from django.shortcuts import render
from .models import Product,Category
from django.shortcuts import get_object_or_404

# Create your views here.
def product_list(request,category_slug=None):
    categories=Category.objects.all()
    products=Product.objects.all(available=True)
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        products=products.filter(category=category)
    return render(request,'shop/product/list.html',{
                        "categories":categories,
                        "category":category,
                        "products":products})

def product_detail(request,id,slug):
    pass