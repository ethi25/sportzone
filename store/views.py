from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    return render(request, 'store/home.html', {
        'categories': categories,
        'products': products
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(available=True)
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {
        'product': product
    })