from .models import Cart

def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart = None
        if request.session.session_key:
            try:
                cart = Cart.objects.get(session_key=request.session.session_key)
            except Cart.DoesNotExist:
                pass
    
    return {
        'cart': cart,
        'cart_item_count': cart.item_count if cart else 0,
        'cart_total': cart.total_price if cart else 0,
    }
