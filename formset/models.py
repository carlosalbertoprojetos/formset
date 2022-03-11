from django.db import models
from autoslug import AutoSlugField
from django.urls import reverse



# ================================================= PRIMEIRO EXEMPLO FORMSET =================================================
# https://www.youtube.com/watch?v=OduVfuv44K8
class Product(models.Model):

    name = models.CharField('Produto', max_length=255, unique=True)
    slug = AutoSlugField(unique=True, always_update=False,
                         populate_from="name")
    image = models.ImageField(
        'Imagem do produto', upload_to="produtos/%Y", blank=True)
    description = models.TextField('Descrição', blank=True)
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    available = models.BooleanField('Disponível', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
  
    def __str__(self):
        return self.name


class Order(models.Model):

    STATUS_CHOICES = [
        ('Pendente', 'pendente'),
        ('Pronto', 'pronto'),
        ('Aguardando', 'aguardando'),
        ('Entregue', 'entregue'),
        ('Cancelado', 'cancelado'),
    ]

    PGTO_CHOICES = [
        ("Pix", "pix"),
        ("Cartão", "cartão"),
        ("Dinheiro", "dinheiro"),
    ]

    withdraw = models.BooleanField('Retirar', default=False)
    data = models.DateField('Data de entrega')
    formpayment = models.CharField(
        'Forma pgto', max_length=11, choices=PGTO_CHOICES)
    total = models.DecimalField('Total', max_digits=11, decimal_places=2, default=0.00, null=True)
    status = models.CharField(
        'Condição', max_length=10, choices=STATUS_CHOICES, default='pendente')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def get_absolute_url_details(self):
        return reverse('formset:order_details', args=[self.pk])
        # return reverse('formset:order_details', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.id)
        

class OrderProducts(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="produto_pedido"
    )
    amount = models.IntegerField('Quantidade', null=True)
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(
        'Subtotal', max_digits=10, decimal_places=2, 
        editable=False, default=0
    )
    details = models.CharField('Detalhes', max_length=300, blank=True)

    def __str__(self):
        return str(self.product)


# ================================================= SEGUNDO EXEMPLO FORMSET =================================================
# https://www.youtube.com/watch?v=JIvJL1HizP4

class Programmer(models.Model):
    
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

    def get_absolute_url_details(self):
        return reverse('formset:programmer_details', args=[self.pk])

class Language(models.Model):
    
    name = models.CharField(max_length=20)
    programmer = models.ForeignKey(Programmer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)