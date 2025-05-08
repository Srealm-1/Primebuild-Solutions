from django.contrib import admin 
from django.urls import path, include
from django.views.generic.base import RedirectView
from Primebuildsolutions import views  # Ensure views is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    # Change this line so root goes directly to the login view
    path('', views.login_view, name='login'),  # <--- EDITED HERE

    path('home/', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    # Include products app URLs with a namespace
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('accounts/', include('django.contrib.auth.urls')),  # Built-in auth views
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
]
