from django.shortcuts import redirect, render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy as _

from .forms import OrderForm
from .models import *


# -------------------(DETAIL/LIST VIEWS) -------------------


def dashboard(request):
    orders = Order.objects.all().order_by('-status')[0:5]
    clients = Client.objects.all()
    total_clients = clients.count()
    total_orders = Order.objects.all().count()
    waiting = Order.objects.filter(status='Aguardando').count()
    pending = Order.objects.filter(status='Pendente').count()
    delivered = Order.objects.filter(status='Enviado').count()

    context = {
        'clients': clients,
        'orders': orders,
        'total_clients': total_clients,
        'total_orders': total_orders,
        'pending': pending,
        'delivered': delivered,
        'waiting': waiting,
    }
    return render(request, 'clientorders/dashboard.html', context)


def product_details(request, pk):
    product = Product.objects.all(pk=pk)
    context = {'product': product}
    return render(request, 'clientorders/products_list.html', context)


def products_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'clientorders/products_list.html', context)


class ClientDetailsView(DetailView):
    model = Client
    template_name = 'clientorders/client_details.html'    

    
client_details = ClientDetailsView.as_view()


def clients_list(request):
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request, 'clientorders/clients_list.html', context)


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
    action = 'create'


client_create = ClientCreateView.as_view()


def order_create(request):
    action = 'create'
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientorders:dashboard')

    context = {'action': action, 'form': form}
    return render(request, 'clientorders/order_create.html', context)


# -------------------(UPDATE VIEWS) -------------------


def order_update(request, pk):
    action = 'update'
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('clientorders:dashboard')

    context = {'action': action, 'form': form}
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
