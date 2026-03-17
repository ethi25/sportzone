from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import Order, OrderItem, Product
from cart.views import get_cart, save_cart

@login_required(login_url='/accounts/login/')
def checkout(request):
    cart = get_cart(request)
    if not cart:
        return redirect('home')

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
            'subtotal': subtotal,
        })

    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total=total)
        for item in cart_items:
            product = Product.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )
        save_cart(request, {})
        return redirect('order_success')

    return render(request, 'checkout/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required(login_url='/accounts/login/')
def order_success(request):
    return render(request, 'checkout/order_success.html')

@login_required(login_url='/accounts/login/')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'checkout/my_orders.html', {'orders': orders})