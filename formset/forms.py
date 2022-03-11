from django import forms
from django.forms.models import inlineformset_factory

from .models import Order, OrderProducts


OrderProductsFormset = inlineformset_factory(Order, OrderProducts, fields=('product', 'amount', 'price', 'details'), extra=2)