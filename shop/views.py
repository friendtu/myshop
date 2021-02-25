from django.shortcuts import render
from .models import Product,Category
from django.shortcuts import get_object_or_404
from cart.forms import CartAddProductForm

# Create your views here.
def product_list(request,category_slug=None):
    category=None
    categories=Category.objects.all()
    products=Product.objects.filter(available=True)
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        products=products.filter(category=category)
    return render(request,'shop/product/list.html',{
                        "categories":categories,
                        "category":category,
                        "products":products})


def product_detail(request,id,slug):
    product=get_object_or_404(Product,id=id,slug=slug,available=True)
    card_add_product_form=CartAddProductForm()

    return render(request,"shop/product/detail.html",
                            {
                                "product":product,
                                'card_add_product_form':card_add_product_form
                            })
    