
from django.urls import path


from .views import (dashboard, 
                   product_create, products_list, product_details, product_update,
                   client_create, clients_list, client_details, client_update, client_dashboard, orders_client_list,
                   order_create, order_update, order_delete
                   )


app_name = 'clientorders'


urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('products/', products_list, name="products_list"),
    path('create/product/', product_create, name="product_create"),
    path('product/<str:pk>/details', product_details, name='product_details'),
    path('product/<str:pk>/update', product_update, name='product_update'),
    
    path('clients/', clients_list, name="clients_list"),
    path('create/client/', client_create, name="client_create"),
    path('client/<int:pk>/dashboard/', client_dashboard, name='client_dashboard'),
    path('client/<int:pk>/details/', client_details, name='client_details'),
    path('client/<str:pk>/update/', client_update, name='client_update'),
    path('client/orders/', orders_client_list, name='orders_client_list'),
    # path('client/orders/create/', client_order_create_formset, name='client_order_create_formset'),
    
    
    path('create/', order_create, name='order_create'),
    path('update/<str:pk>/', order_update, name='order_update'),
    path('delete/<str:pk>/', order_delete, name='order_delete'),
]
