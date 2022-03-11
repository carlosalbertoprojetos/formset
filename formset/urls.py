from django.urls import path

from .views import (add_language, add_language2, add_language3,order_create, order_details,
                    order_products_update, programmer_details,
                    orders_list, programmer_list, programmer_create)

app_name = 'formset'


urlpatterns = [
    path('register/', order_create, name='order_create'),
    path('list/', orders_list, name='orders_list'),
    path('<int:pk>/detail/', order_details, name='order_details'),
    path('<int:pk>/detail/products/update/',
         order_products_update, name='order_products_update'),

    # ================================================= SEGUNDO EXEMPLO FORMSET =================================================
    path('programmer/register/', programmer_create, name='programmer_create'),    
    path('programmers/', programmer_list, name='programmer_list'),
    path('<programmer_id>/programmer/', add_language, name='add_language'),    
    path('<programmer_id>/programmer2/', add_language2, name='add_language2'),
     path('<programmer_id>/programmer3/', add_language3, name='add_language3'),
    path('<int:pk>/programmer/detail/',
         programmer_details, name='programmer_details'),
]
