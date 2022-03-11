from django.urls import path


from .views import orders_list, orders_products_list, order_create, order_details, order_products_update


app_name = 'formset'


urlpatterns = [
    path('register/', order_create, name='order_create'),
    path('list/', orders_list, name='orders_list'),
    path('<int:pk>/detail/', order_details, name='order_details'),
    path('<int:pk>/detail/products/update/', order_products_update, name='order_products_update'),
]




