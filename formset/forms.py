from django import forms
from django.forms.models import inlineformset_factory

from .models import Order, OrderProducts, Cliente, Telefone


OrderProductsFormset = inlineformset_factory(Order, OrderProducts, fields=('product', 'amount', 'price', 'details'), extra=2)



# ================================================= TERCEIRO EXEMPLO FORMSET =================================================

class ClienteForm(forms.ModelForm):
    class Meta:        
        model = Cliente
        fields = '__all__'


class TelefoneFormset(forms.ModelForm):
    class Meta:        
        model = Telefone
        fields = '__all__'