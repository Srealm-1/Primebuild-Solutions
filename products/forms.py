from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            # Add any other fields you want to appear in the form, e.g.:
            # 'stock_quantity',
            # 'is_active',
        ]
