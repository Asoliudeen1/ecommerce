from django.shortcuts import redirect, render, get_object_or_404
from cart.models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    """
      Retrieve or create a session key for the cart.

      If the session key does not exist, a new session is created.

      Args:
          request: The HTTP request object.

      Returns:
          str: The session key representing the cart ID.
    """

    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_cart(request, product_id):
    """
    Handles adding a product to the cart, including variations (e.g., size, color).

    Steps:
    1. Retrieve the selected product.
    2. Extract variations (size & color) from the request.
    3. Get or create the shopping cart using the session-based cart_id.
    4. Check if the product already exists in the cart:
        - If yes: Update variations & increase quantity.
        - If no: Create a new cart item and attach variations.
    5. Redirect the user to the cart page.

    Args:
        request (HttpRequest): The HTTP request containing form data.
        product_id (int): The ID of the product being added.

    Returns:
        HttpResponseRedirect: Redirects the user to the cart page after adding the item.
    """

    product = get_object_or_404(Product, id=product_id)

    # Variation (Color and Size)
    product_variation = []
    if request.method == "POST":
        for key in request.POST:
            key = key
            value = request.POST.get(key)
            try:
                variation = Variation.objects.get(
                    product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )

    is_cart_item_exists = CartItem.objects.filter(
        product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)

        # existing Variations -> database
        #  Current Variation -> product_variation (list)
        #  Item_id -> databse

        ex_var_list = []
        ids = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            ids.append(item.id)

        if product_variation in ex_var_list:
            # Increase the Cart Item Quantity
            index = ex_var_list.index(product_variation)
            item_id = ids[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()

        else:
            item = CartItem.objects.create(
                product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()

    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )

        # add Variation to CartItem
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(
        product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request):
    """
    Retrieve cart details, including total price and quantity.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the cart page with total cost, quantity, and cart items.
    """

    total = 0
    quantity = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        total = sum(cart_item.product.price *
                    cart_item.quantity for cart_item in cart_items)
        quantity = sum(cart_item.quantity for cart_item in cart_items)

        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        cart = []

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'cart/cart.html', context)
