from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('update_cart/', views.update_cart, name='update_cart'),
    
    # Payment routes
    path('orders/payment/<str:method>/', views.payment, name='payment'),
    path("payment/success/", views.payment_success_view, name="payment_success"),
    path("payment/failed/", views.payment_failed_view, name="payment_failed"),
    path("mpesa_payment/", views.mpesa_payment, name="mpesa_payment"),
    path("credit_payment/", views.credit_payment, name="credit_payment"),
path('confirm_payment/', views.confirm_payment_view, name='confirm_payment'),

    
    # Order history (removed duplicate)
    path('order-history/', views.order_history, name='order_history'),
]
