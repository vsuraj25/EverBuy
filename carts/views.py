from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def get_tax(amount, tax_perc = 2):
    return (tax_perc * amount)/ 100

def cart(request):
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active =True)
        total, quantity = 0, 0
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

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.cart_quantity += 1
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product, 
            cart=cart, 
            cart_quantity = 1
        )

        cart_item.save()

    return redirect('cart')

def remove_product_from_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart = cart)
    if cart_item.cart_quantity > 1:
        cart_item.cart_quantity -= 1
        cart_item.save()
    else:
        cart.delete()
    return redirect('cart')