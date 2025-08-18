from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe
from decimal import Decimal
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.views import get_or_create_cart

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart_detail')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            order.user = request.user
            order.cart = cart
            
            # Calculate totals
            subtotal = cart.total_price
            tax = subtotal * Decimal('0.08')  # 8% tax
            shipping = Decimal('10.00') if subtotal < Decimal('100.00') else Decimal('0.00')
            total = subtotal + tax + shipping
            
            order.subtotal = subtotal
            order.tax = tax
            order.shipping = shipping
            order.total = total
            order.save()
            
            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    product_price=cart_item.product.current_price,
                    quantity=cart_item.quantity,
                    total_price=cart_item.total_price
                )
            
            # Create Stripe payment intent
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(total * 100),  # Convert to cents
                    currency='usd',
                    metadata={
                        'order_id': order.id,
                        'order_number': order.order_number,
                    }
                )
                order.stripe_payment_intent = intent.id
                order.save()
                
                return render(request, 'orders/payment.html', {
                    'order': order,
                    'client_secret': intent.client_secret,
                    'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
                })
                
            except stripe.error.StripeError as e:
                messages.error(request, f'Payment error: {str(e)}')
                order.delete()
                return redirect('checkout')
    else:
        form = CheckoutForm(user=request.user)
    
    context = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_list(request):
    orders = request.user.orders.all()
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)

@csrf_exempt
@require_POST
def payment_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata']['order_id']
        
        try:
            order = Order.objects.get(id=order_id)
            order.payment_status = 'paid'
            order.status = 'processing'
            order.save()
            
            # Clear the cart after successful payment
            order.cart.items.all().delete()
            
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata']['order_id']
        
        try:
            order = Order.objects.get(id=order_id)
            order.payment_status = 'failed'
            order.status = 'cancelled'
            order.save()
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
    
    return JsonResponse({'status': 'success'})

def payment_success(request):
    payment_intent_id = request.GET.get('payment_intent')
    if payment_intent_id:
        try:
            order = Order.objects.get(stripe_payment_intent=payment_intent_id)
            messages.success(request, f'Payment successful! Order #{order.order_number}')
            return render(request, 'orders/payment_success.html', {'order': order})
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
    
    return redirect('home')

def payment_cancel(request):
    messages.warning(request, 'Payment was cancelled.')
    return redirect('cart_detail')
