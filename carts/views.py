from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def get_tax(amount, tax_perc = 2):
    return (tax_perc * amount)/ 100

def cart(request):
    total, quantity, tax, grand_total = 0, 0, 0, 0
    cart_items = {}
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active =True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.cart_quantity)
            quantity += cart_item.cart_quantity

        tax = get_tax(total)
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'store/cart.html', context)

def add_product_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        for key in request.POST:
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product =product, variation_category = key, variation_value = value)
                product_variation.append(variation)
            except:
                pass
    
    ## Getting the requested product ID
    product = Product.objects.get(id=product_id)

    try:
        ## Getting the cart id i.e. session_id
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )

    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart = cart).exists()

    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        
        existing_variations_list = []
        ids = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_variations_list.append(list(existing_variation))
            ids.append(item.id)
            
        if product_variation in existing_variations_list:
            ## increase the cart item quantity
            idx = existing_variations_list.index(product_variation)
            item_id = ids[idx]
            item = CartItem.objects.get(product=product, id=item_id)
            item.cart_quantity += 1
            item.save()
        else:
            ## create a new cart item
            item = CartItem.objects.create(product=product, cart_quantity = 1, cart = cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)

            # item.cart_quantity += 1
            item.save()

    else:
        cart_item = CartItem.objects.create(
            product=product, 
            cart=cart, 
            cart_quantity = 1
        )

        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)

        cart_item.save()

    return redirect('cart')

def remove_product_from_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart = cart, id = cart_item_id)
        if cart_item.cart_quantity > 1:
            cart_item.cart_quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart, id = cart_item_id)
    cart_item.delete()
    return redirect('cart')

    