
from django.forms import inlineformset_factory, modelformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls import reverse_lazy as _
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView

from .forms import OrderProductsFormset, ClienteForm, TelefoneFormset
from .models import Language, Order, OrderProducts, Programmer, Cliente, Telefone


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


# ================================================= SEGUNDO EXEMPLO FORMSET =================================================

class ProgrammerCreateView(CreateView):
    
    model = Programmer
    fields = '__all__'
    success_url = _('formset:programmer_list')
    template_name = 'programmer_register.html'

programmer_create = ProgrammerCreateView.as_view()


class ProgrammerListView(ListView):
    
    model = Programmer
    template_name = 'programmer_list.html'

programmer_list = ProgrammerListView.as_view()


class ProgrammerDetailsView(DetailView):
    model = Programmer
    template_name = 'programmer_details.html'

programmer_details = ProgrammerDetailsView.as_view()



# 1) modelformset_factory
def add_language(request, programmer_id):
    programmer = Programmer.objects.get(pk=programmer_id)
    LanguageFormset = modelformset_factory(Language, fields=('name',), extra=2)
    
    if request.method == 'POST':
        formset = LanguageFormset(request.POST, queryset=Language.objects.filter(programmer__id=programmer.id))    
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.programmer_id = programmer.id
                instance.save()
                
            return redirect('formset:add_language', programmer_id=programmer.id)  
        
        
    formset = LanguageFormset(queryset=Language.objects.filter(programmer__id=programmer.id))
    
    return render(request, 'language_model.html', {'formset':formset})
    
    
 
 # 2) inlineformset_factory
def add_language2(request, programmer_id):
    programmer = Programmer.objects.get(pk=programmer_id)
    LanguageFormset = inlineformset_factory(Programmer, Language, fields=('name',), extra=2)
    
    if request.method == 'POST':
        formset = LanguageFormset(request.POST, instance=programmer)  
        if formset.is_valid():
            formset.save()
            return redirect('formset:add_language2', programmer_id=programmer.id)        
        
    formset = LanguageFormset(instance=programmer)  
    
    return render(request, 'language_inline.html', {'formset':formset})


 # 3) inlineformset_factory - 2º exemplo
# opções: delete, extra e max_num
def add_language3(request, programmer_id):
    programmer = Programmer.objects.get(pk=programmer_id)
    LanguageFormset = inlineformset_factory(Programmer, Language, fields=('name',), can_delete=False, extra=2, max_num=5)

    if request.method == 'POST':
        formset = LanguageFormset(request.POST, instance=programmer)  
        if formset.is_valid():
            formset.save()
            return redirect('formset:add_language3', programmer_id=programmer.id)
        
    formset = LanguageFormset(instance=programmer)  

    return render(request, 'language_inline.html', {'formset':formset})
 
 
# ================================================= TERCEIRO EXEMPLO FORMSET =================================================
 
def clientes_list(request):
    cliente = Cliente.objects.all()
    context = {
        'cliente': cliente,
    }
    return render(request, 'clientes_list.html', context)
    
    
def cliente_details(request, pk):
    cliente = Cliente.objects.filter(pk=pk)
    context = {
        'cliente': cliente,
    }
    return render(request, 'cliente_details.html', context)
    

def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        Form_Telefone_Factory = inlineformset_factory(Cliente, Telefone, form=TelefoneFormset)
        form_telefone = Form_Telefone_Factory(request.POST)
        if form.is_valid() and form_telefone.is_valid():
            cliente = form.save()
            form_telefone.instance = cliente
            form_telefone.save()
            return redirect('formset:cliente_update', id=cliente.id)
        
        else:
            context = {
                'form': form,
                'form_telefone':form_telefone
            }
            return render(request, 'clientes_list.html', context)
    
    elif request.method == 'GET':
        form = ClienteForm()
        Form_Telefone_Factory = inlineformset_factory(Cliente, Telefone, form=TelefoneFormset, extra=3)
        form_telefone = Form_Telefone_Factory()
        context = {
            'form': form,
            'form_telefone':form_telefone
        }
        return render(request, 'cliente_create.html', context)



def cliente_update(request, id):
    if request.method == 'POST':
        cliente = Cliente.objects.filter(id=id).first()
        if cliente is None:
            return redirect('formset:clientes_list')
        
        form = ClienteForm(request.POST, instance=cliente)
        Form_Telefone_Factory = inlineformset_factory(Cliente, Telefone, form=TelefoneFormset, extra=3)
        form_telefone = Form_Telefone_Factory(request.POST, instance=cliente)
        if form.is_valid() and form_telefone.is_valid():
            form.save()
            form_telefone.save()
            return redirect('formset:cliente_update', id=id)
        
        else:
            context = {
                'form': form,
                'form_telefone':form_telefone
         }
        return render(request, 'cliente_update.html', context)
        
    elif request.method == 'GET':
        cliente = Cliente.objects.filter(id=id).first()
        if cliente is None:
            return redirect('formset:clientes_list')
        
        form = ClienteForm(instance=cliente)
        Form_Telefone_Factory = inlineformset_factory(Cliente, Telefone, form=TelefoneFormset, extra=3)
        form_telefone = Form_Telefone_Factory(instance=cliente)
        context = {
            'form': form,
            'form_telefone':form_telefone
        }
        return render(request, 'cliente_update.html', context)
