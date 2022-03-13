from django.contrib import admin


from . models import Client, Order, Product

admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Order)
