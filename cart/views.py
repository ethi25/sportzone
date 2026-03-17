from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product

def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    pid = str(product_id)
    if pid in cart:
        cart[pid]['quantity'] += 1
    else:
        cart[pid] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1,
            'slug': product.slug,
        }
    save_cart(request, cart)
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
    save_cart(request, cart)
    return redirect('cart_detail')

def update_cart(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart[pid]['quantity'] = quantity
    else:
        del cart[pid]
    save_cart(request, cart)
    return redirect('cart_detail')

def cart_detail(request):
    cart = get_cart(request)
    cart_items = []
    total = 0
    for id, item in cart.items():
        subtotal = float(item['price']) * item['quantity']
        total += subtotal
        cart_items.append({
            'id': id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'slug': item['slug'],
            'subtotal': subtotal,
        })
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total})