from cart.views import _cart_id
from .models import CartItem, Cart

def counter(request):
  """
  Returns the total number of items in the user's shopping cart.

  This function checks if the request is from the Django admin panel and returns 
  an empty dictionary if true. Otherwise, it retrieves the cart associated with 
  the user's session, counts the total quantity of items, and returns it as a 
  context variable.

  Args:
      request (HttpRequest): The incoming HTTP request.

  Returns:
      dict: A dictionary containing the cart item count, e.g., {'cart_count': 3}.
  """
  
  cart_count=0
  if request.path.startswith('/admin/'):
    return {}
  
  cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
  if cart:
    cart_items = CartItem.objects.filter(cart=cart)
    cart_count = sum(cart_item.quantity for cart_item in cart_items)
   
  return {'cart_count':cart_count}