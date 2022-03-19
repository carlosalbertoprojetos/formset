from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls import reverse_lazy as _
from django.views.generic.edit import CreateView, UpdateView

from .forms import ClientOrderForm, OrderForm, OrderProductsForm
from .models import Client, Order, OrderProducts, Product

# -------------------(DETAIL/LIST VIEWS) -------------------


def dashboard(request):
    clients = Client.objects.all()
    orders = Order.objects.all().order_by('-status')[0:5]
    total_clients = clients.count()
    total_orders = Order.objects.all().count()
    waiting = Order.objects.filter(status='Aguardando').count()
    pending = Order.objects.filter(status='Pendente').count()
    sent = Order.objects.filter(status='Enviado').count()

    context = {
        'clients': clients,
        'orders': orders,
        'total_clients': total_clients,
        'total_orders': total_orders,
        'pending': pending,
        'sent': sent,
        'waiting': waiting,
    }
    return render(request, 'clientorders/dashboard.html', context)


def client_dashboard(request, pk):
    client = list(Client.objects.filter(pk=pk))
    orders = Order.objects.filter(client_id=pk).order_by('-status')[0:10]
    total_orders = Order.objects.filter(client_id=pk).count()
    waiting = Order.objects.filter(client_id=pk, status='Aguardando').count()
    pending = Order.objects.filter(client_id=pk, status='Pendente').count()
    sent = Order.objects.filter(client_id=pk, status='Enviado').count()
    delivered = Order.objects.filter(client_id=pk, status='Entregue').count()
    template_name = ('clientorders/client_dashboard.html', pk)

    context = {
        'client': client,
        'orders': orders,
        'total_orders': total_orders,
        'pending': pending,
        'sent': sent,
        'waiting': waiting,
        'delivered': delivered,
    }
    return render(request, template_name, context)


def product_details(request, pk):
    product = Product.objects.all(pk=pk)
    context = {'product': product}
    return render(request, 'clientorders/products_list.html', context)


def products_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'clientorders/products_list.html', context)


def client_details(request, pk):
    objects = Client.objects.filter(pk=pk)
    context = {'objects': objects}
    return render(request, 'clientorders/client_details.html', context)


def clients_list(request):
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request, 'clientorders/clients_list.html', context)


def orders_client_list(request, pk):
    client = Client.objects.filter(pk=pk)
    orders = Order.objects.all()
    context = {
        'client': client,
        'orders': orders
    }
    return render(request, 'clientorders/order_client_list.html', context)


# -------------------(CREATE VIEWS) -------------------


class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    template_name = 'clientorders/product_create.html'
    success_url = _('clientorders:products_list')


product_create = ProductCreateView.as_view()


class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    template_name = 'clientorders/client_create.html'
    success_url = _('clientorders:clients_list')


client_create = ClientCreateView.as_view()


# def order_create(request):
#     form = OrderForm()

#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('clientorders:dashboard')

#     context = {
#         'form': form
#     }
#     return render(request, 'clientorders/order_create.html', context)


def client_order_create(request, pk):
    form = ClientOrderForm()

    if request.method == 'POST':
        form = ClientOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client_id = pk
            order.save()
            return redirect('clientorders:dashboard')

    context = {
        'form': form
    }
    return render(request, 'clientorders/order_create.html', context)


def order_create(request):

    if request.method == 'POST':
        form = OrderForm(request.POST)

        Products_Order_Factory = inlineformset_factory(
            Order, OrderProducts, form=OrderProductsForm, extra=3)
        form_order_products = Products_Order_Factory(request.POST)

        if form.is_valid() and form_order_products.is_valid():
            order = form.save()
            # order.client_id = pk
            # order.save()
            form_order_products.instance = order
            form_order_products.save()
            return redirect('clientorders:clients_list')

        else:
            context = {
                'form': form,
                'form_order_products': form_order_products
            }
            return render(request, 'clientorders/order_create.html', context)

    elif request.method == 'GET':
        form = OrderForm()
        
        Products_Order_Factory = inlineformset_factory(
            Order, OrderProducts, form=OrderProductsForm, extra=3)
        form_order_products = Products_Order_Factory()

        context = {
            'form': form,
            'form_order_products': form_order_products
        }
        return render(request, 'clientorders/order_create.html', context)


# -------------------(UPDATE VIEWS) -------------------


def order_update(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()

    context = {
        'form': form
    }
    return render(request, 'clientorders/order_update.html', context)


# -------------------(DELETE VIEWS) -------------------


class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'clientorders/product_update.html'

    def get_success_url(self):
        return reverse('clientorders:product_update', kwargs={'pk': self.object.pk})


product_update = ProductUpdateView.as_view()


class ClientUpdateView(UpdateView):
    model = Client
    fields = '__all__'
    template_name = 'clientorders/client_update.html'

    def get_success_url(self):
        return reverse('clientorders:client_update', kwargs={'pk': self.object.pk})


client_update = ClientUpdateView.as_view()


def order_delete(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        client_id = order.client.id
        client_url = '/client/' + str(client_id)
        order.delete()
        return redirect(client_url)

    return render(request, 'clientorders/delete_item.html', {'item': order})
