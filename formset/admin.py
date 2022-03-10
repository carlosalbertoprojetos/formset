from django.contrib import admin

from .models import Product, Orders, OrderProducts




class OrderProductsAdmin(admin.TabularInline):
    model = OrderProducts
    extra = 1
    readonly_fields = ['subtotal', ]


class OrderAdmin(admin.ModelAdmin):

    date_hierarchy = 'created_at'
    # list_filter = ['client', 'created_at', 'status']
    # search_fields = ['client', 'created_at', 'formpayment']
    readonly_fields = ['created_at', 'total']
    # list_display = ['client', 'created_at', 'formpayment',
    #                 'status', 'data', 'status']
    list_display = ['created_at', 'formpayment', 'status', 'data', 'status']
    # readonly_fields = ['client']
    inlines = [
        OrderProductsAdmin,
    ]


admin.site.register(Orders, OrderAdmin)


admin.site.register(Product)
