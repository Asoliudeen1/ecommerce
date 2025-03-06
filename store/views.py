from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category


def store(request, category_slug=None):
  products = Product.objects.filter(is_available=True)
  

  if category_slug:
    category = get_object_or_404(Category, slug=category_slug)
    products = products.filter(category=category)
   
  context = {
    'products':products,
    'total_products': products.count()
  }
  return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
  # product = get_object_or_404(category__slug=category_slug, slug=product_slug)
  product = get_object_or_404(Product.objects.select_related('category'), category__slug=category_slug, slug=product_slug)
  
  context={
    'product':product,
  }
  return render(request, 'store/product_detail.html', context)