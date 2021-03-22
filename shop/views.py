from django.shortcuts import render
from .models import Product,Category
from django.shortcuts import get_object_or_404
from cart.forms import CartAddProductForm
from .recommender import Recommender

# Create your views here.
def product_list(request,category_slug=None):
    category=None
    categories=Category.objects.all()
    products=Product.objects.filter(available=True)
    language=request.LANGUAGE_CODE
    if category_slug:
        category=get_object_or_404(Category,translations__language_code=language,translations__slug=category_slug)
        products=products.filter(category=category)
    return render(request,'shop/product/list.html',{
                        "categories":categories,
                        "category":category,
                        "products":products})


def product_detail(request,id,slug):
    language=request.LANGUAGE_CODE
    product=get_object_or_404(Product,translations__language_code=language,id=id,translations__slug=slug,available=True)
    cart_add_product_form=CartAddProductForm()
    r=Recommender()
    recommented_products=r.suggest_products_for([product],4)
    
    return render(request,"shop/product/detail.html",
                            {
                                "product":product,
                                'cart_add_product_form':cart_add_product_form,
                                'recommented_products':recommented_products
                            })
    