from django.urls import path

from .views import (order_create, orders_list, order_details, order_products_update,
                    programmer_create, programmer_list, programmer_details, add_language, add_language2, add_language3, 
                    cliente_create, clientes_list, cliente_details, cliente_update
                    )

app_name = 'formset'


urlpatterns = [
    path('register/', order_create, name='order_create'),
    path('list/', orders_list, name='orders_list'),
    path('<int:pk>/detail/', order_details, name='order_details'),
    path('<int:pk>/detail/products/update/',
         order_products_update, name='order_products_update'),

    # ================================================= SEGUNDO EXEMPLO FORMSET =================================================
    path('programmer/create/', programmer_create, name='programmer_create'),    
    path('programmers/', programmer_list, name='programmer_list'),
    path('<programmer_id>/programmer/', add_language, name='add_language'),    
    path('<programmer_id>/programmer2/', add_language2, name='add_language2'),
    path('<programmer_id>/programmer3/', add_language3, name='add_language3'),
    path('<int:pk>/programmer/detail/',
         programmer_details, name='programmer_details'),
    
#     fazer o update
    
    # ================================================= TERCEIRO EXEMPLO FORMSET =================================================
    path('cliente/create/', cliente_create, name='cliente_create'), 
    path('clientes/list/', clientes_list, name='clientes_list'),
    path('<int:pk>/details/cliente/', cliente_details, name='cliente_details'),  
    path('<int:id>/update/cliente/',
         cliente_update, name='cliente_update'),   
]
