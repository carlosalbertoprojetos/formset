
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy as _
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView

from .forms import OrderProductsFormset
from .models import Order, OrderProducts, Product


class OrdersListView(ListView):
    model = Order
    template_name = 'orders_list.html'

orders_list = OrdersListView.as_view()



class OrderProductsListView(ListView):
    
    model = OrderProducts
    template_name = 'order_products_list.html'

orders_products_list = OrderProductsListView.as_view()



class OrderCreateView(CreateView):
    
    model = Order
    template_name = 'order_create.html'
    fields = '__all__'
    success_url = _('formset:orders_list')

order_create = OrderCreateView.as_view()



class OrderDetailsView(DetailView):
    model = Order
    template_name = 'order_details.html'

order_details = OrderDetailsView.as_view()



class OrderProductsUpdateView(SingleObjectMixin, FormView):

    model = Order
    template_name = 'order_update_products.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Order.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Order.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return OrderProductsFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('formset:order_details', kwargs={'pk': self.object.pk})


order_products_update = OrderProductsUpdateView.as_view()
