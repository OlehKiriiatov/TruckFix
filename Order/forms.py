from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['truck_model', 'location', 'phone_number', 'description', 'file']