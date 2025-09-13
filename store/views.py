from django.shortcuts import render
from .models import Product 

def store(request):
    
    products = Product.objects.all().filter(is_available =True)

    context = {
        'products': products,
        'products_count': len(products)
    }

    return render(request, 'store/store.html', context)
