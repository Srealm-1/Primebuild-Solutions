from django import forms
from .models import OrderItem, Order

class CartItemForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, label="Quantity")

    class Meta:
        model = OrderItem
        fields = ['quantity']

class CheckoutForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('MPESA', 'M-Pesa'),
        ('CARD', 'Credit/Debit Card'),
        ('CASH', 'Cash on Delivery')
    ]

    phone_number = forms.CharField(
        max_length=15,
        label="Phone Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        label="Payment Method"
    )

    class Meta:
        model = Order
        fields = ['user', 'phone_number', 'payment_method']
        widgets = {
            'user': forms.HiddenInput(),
        }
