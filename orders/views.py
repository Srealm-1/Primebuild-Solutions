from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm
from products.models import Product  
import json
from django.http import HttpResponse
from django.urls import reverse
import logging
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('orders:cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('orders:cart')

@login_required
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total_price=cart.total_price(),
                phone_number=form.cleaned_data['phone_number'],
                payment_method=form.cleaned_data['payment_method'],
                status="Pending"
            )
            for cart_item in cart.cart_items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Store Order ID in session and redirect to payment page
            request.session['order_id'] = order.id
            return redirect('orders:payment', method=order.payment_method)

    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {'form': form})

@login_required
def payment_view(request, method):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('orders:checkout')

    return render(request, 'orders/payment.html', {'payment_method': method})

@login_required
def confirm_payment_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone = data.get("phone")
            amount = data.get("amount")

            order_id = request.session.get('order_id')

            if order_id:
                order = Order.objects.get(id=order_id, user=request.user)
                if str(order.total_price) == amount:  # Ensure amount matches
                    order.status = "Paid"
                    order.save()
                    del request.session['order_id']  # Clear session after payment
                    
                    return JsonResponse({"status": "success", "redirect_url": "/orders/payment_success/"})
                else:
                    return JsonResponse({"status": "failed", "message": "Amount mismatch"})
            
            # If no order is found, still redirect to success page
            return JsonResponse({"status": "success", "redirect_url": "/orders/payment_success/"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "failed", "message": "Invalid request"})

    return JsonResponse({"status": "failed", "message": "Invalid request method"})


@login_required
def payment_success_view(request):
    order_id = request.session.get('order_id')
    if order_id:
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            order.status = "Paid"
            order.save()
        except Order.DoesNotExist:
            # Order not found; proceed to render the success page regardless.
            pass
        finally:
            # Clear session after payment (even if the order was not found)
            if 'order_id' in request.session:
                del request.session['order_id']
                
    return render(request, 'orders/payment_success.html')

@login_required
def payment_failed_view(request):
    return render(request, 'orders/payment_failed.html')


@login_required
def order_history(request):
    # Get all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'order_history.html', context)

def update_cart(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("quantity_"):
                cart_item_id = key.split("_")[1]
                cart_item = get_object_or_404(CartItem, id=cart_item_id)
                cart_item.quantity = int(value)
                cart_item.save()
    return redirect("orders:cart")

@login_required
def mpesa_payment(request):
    phone = request.GET.get("phone", "")  # Retrieve phone number from GET params
    amount = request.GET.get("amount","500") # Replace this with actual order total calculation

    context = {
        "phone": phone,
        "amount": amount,  # Ensure amount is passed
    }
    return render(request, "orders/mpesa_payment.html", context)

@login_required
def credit_payment(request):
    return render(request, "orders/credit_payment.html")

def mpesa_callback(request):
    if request.method == 'POST':
        data = request.POST  # or request.body if JSON
        phone_number = data.get('phone_number')
        amount = data.get('amount')
        order = Order.objects.filter(phone_number=phone_number, amount=amount).first()
        
        if order:
            order.payment_status = True
            order.save()
            return JsonResponse({'message': 'Payment successful!'}, status=200)

    return JsonResponse({'message': 'Payment failed!'}, status=400)

@login_required
def payment(request, method):
    if request.method == "POST":
        # Handle MPESA payment
        if method == "MPESA":
            phone = request.POST.get("phone")
            amount = request.POST.get("amount")

            # Debugging: Check if data is captured
            print(f"Processing MPESA payment for {phone} amount {amount}")

            # Simulate processing (Replace this with actual API call to MPESA)
            payment_status = True  # Simulating a successful payment

            if payment_status:
                return redirect("orders:order_history")  # Redirect to order history
            else:
                return redirect("orders:payment_failed")

    return HttpResponse("Invalid Payment Request")