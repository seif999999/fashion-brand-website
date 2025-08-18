from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .models import Cart, CartItem
from decimal import Decimal

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, available=True)
        cart = get_or_create_cart(request)
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if product is already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'{product.name} added to cart!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{product.name} added to cart!',
                'cart_count': cart.item_count
            })
        
        return redirect('cart_detail')
    
    return redirect('product_detail', slug=product.slug)

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = cart_item.cart
    
    # Check if user owns this cart
    if request.user.is_authenticated and cart.user != request.user:
        messages.error(request, 'You do not have permission to modify this cart.')
        return redirect('cart_detail')
    
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart!')
    
    return redirect('cart_detail')

def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart = cart_item.cart
        
        # Check if user owns this cart
        if request.user.is_authenticated and cart.user != request.user:
            messages.error(request, 'You do not have permission to modify this cart.')
            return redirect('cart_detail')
        
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_total': cart.total_price,
                'cart_count': cart.item_count
            })
    
    return redirect('cart_detail')

def cart_detail(request):
    cart = get_or_create_cart(request)
    
    # Calculate tax and shipping
    subtotal = cart.total_price
    tax_rate = Decimal('0.08')  # 8%
    tax_amount = subtotal * tax_rate
    shipping_cost = Decimal('0') if subtotal >= Decimal('100') else Decimal('10.00')
    total = subtotal + tax_amount + shipping_cost
    
    context = {
        'cart': cart,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'shipping_cost': shipping_cost,
        'total': total,
    }
    return render(request, 'cart/cart_detail.html', context)

def clear_cart(request):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        messages.success(request, 'Cart cleared successfully!')
    
    return redirect('cart_detail')
