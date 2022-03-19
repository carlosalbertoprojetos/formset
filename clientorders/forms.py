from django.forms import ModelForm

from .models import Order, OrderProducts


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class OrderProductsForm(ModelForm):
    class Meta:
        model = OrderProducts
        fields = '__all__'


class ClientOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['client']
