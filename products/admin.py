# products/admin.py
from django.contrib import admin
from django.db.models import F
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import format_html
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 1. Correct list_display using your actual model fields
    list_display = [
        'name',
        'sku',
        'price',
        'stock_quantity',
        'available_quantity_column',
        'stock_status',
        'is_active',
        'updated_at'
    ]
    
    # 2. Fields to show in edit view
    fields = [
        'name',
        'description',
        'sku',
        'price',
        'stock_quantity',
        'is_active'
    ]
    
    # 3. Proper filtering and searching
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'sku', 'description']
    
    # 4. Custom actions
    actions = ['restock_products', 'toggle_active_status']

    # 5. Custom columns
    @admin.display(description='Available')
    def available_quantity_column(self, obj):
        """Shows available quantity (same as stock_quantity in your case)"""
        return obj.stock_quantity

    @admin.display(description='Status')
    def stock_status(self, obj):
        """Color-coded stock status indicator"""
        if obj.stock_quantity <= 0:
            return format_html('<span style="color: red">Out of Stock</span>')
        elif obj.stock_quantity <= 5:
            return format_html('<span style="color: orange">Low Stock</span>')
        return format_html('<span style="color: green">In Stock</span>')

    # 6. Custom actions
    @admin.action(description='Restock selected products (+50 units)')
    def restock_products(self, request, queryset):
        queryset.update(stock_quantity=F('stock_quantity') + 50)

    @admin.action(description='Toggle active status')
    def toggle_active_status(self, request, queryset):
        queryset.update(is_active=~F('is_active'))

    # 7. Stock dashboard (optional)
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('stock-dashboard/', self.admin_site.admin_view(self.stock_dashboard))
        ]
        return custom_urls + urls

    def stock_dashboard(self, request):
        context = {
            'low_stock': Product.objects.filter(stock_quantity__lt=5),
            'out_of_stock': Product.objects.filter(stock_quantity=0),
            'total_products': Product.objects.count()
        }
        return TemplateResponse(
            request,
            'products/admin/products/stock_dashboard.html',
context = {'products': Product.objects.all()}
)

    # 8. Auto-refresh (optional)
    class Media:
        js = ('js/admin_auto_refresh.js',)
        css = {
            'all': ('css/admin_stock.css',)
        }