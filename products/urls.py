from django.urls import path
from .views import (
    product_list,
    product_detail,
    product_create,
    product_update,
    product_delete,
    login_view,  # <-- Added login_view import
)

app_name = 'products'  # Namespace for URL reversal

urlpatterns = [
    path('login/', login_view, name='login'),  # <-- Added login URL pattern
    path('', product_list, name='list'),  # Product list view
    path('create/', product_create, name='product_create'),  # Create a new product
    path('<int:pk>/', product_detail, name='product_detail'),  # CHANGED name='detail' to name='product_detail'
    path('<int:pk>/update/', product_update, name='update'),  # Update product
    path('<int:pk>/delete/', product_delete, name='delete'),  # Delete product
]
