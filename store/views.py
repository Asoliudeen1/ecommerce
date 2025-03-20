from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from cart.models import CartItem
from cart.views import _cart_id
from .models import Product
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


def store(request, category_slug=None):

  if category_slug:
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

  else:
    products = Product.objects.filter(is_available=True)  

  paginator = Paginator(products, 8)
  page = request.GET.get('page')
  paged_products = paginator.get_page(page)


    
  context = {
    'products':paged_products,
    'total_products': products.count()
  }
  return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):
  # product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
  product = get_object_or_404(Product.objects.select_related('category'), category__slug=category_slug, slug=product_slug)
  in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product)

  variations = product.variation_set.all()
  
  
  context={
    'product':product,
    'in_cart':in_cart,
    # 'variations': variations,
  }
  return render(request, 'store/product_detail.html', context)




def search(request):
    """
    Handles product search functionality.

    This function retrieves products based on a search keyword provided by the user.
    It checks if a 'keyword' parameter exists in the request's GET data, and if it does,
    it filters products whose names contain the keyword (case-insensitive).
    
    Steps:
    1. Fetch all available products by default.
    2. Check if 'keyword' exists in request.GET.
    3. If 'keyword' exists, retrieve and strip whitespace from it.
    4. If the keyword is not empty, filter products based on `product_name__icontains=keyword`.
    5. Pass the filtered product list to the template for rendering.

    Args:
        request (HttpRequest): The HTTP request object containing search parameters.

    Returns:
        HttpResponse: Renders the `store/store.html` template with the filtered products.

    Example Usage:
        - User visits: `/store/search/?keyword=shoes`
        - The function filters products that contain "shoes" in their name (case-insensitive).
    """

    products = Product.objects.filter(is_available=True)  # Default queryset

    if 'keyword' in request.GET:  
        keyword = request.GET.get('keyword', '').strip() 
        if keyword: 
            products = products.filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))

    context = {'products': products,
               'total_products': products.count(),}
    return render(request, 'store/store.html', context)
