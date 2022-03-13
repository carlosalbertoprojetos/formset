from autoslug import AutoSlugField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


class Client(models.Model):

    ETNIA_CHOICES = [
        ("Português", "português"),
        ("Brasileiro", "brasileiro"),
        ("Africano", "africano"),
    ]

    STATUS_CHOICES = [
        ("Ativo", "ativo"),
        ("Inativo", "inativo"),
    ]

    PROVINCIA_CHOICES = [
        ("Ag", "Algarve"),
        ("Al", "Alto Alentejo"),
        ("Ba", "Baixo Alentejo"),
        ("Be", "Beira Alta"),
        ("Bx", "Beira Baixa"),
        ("Bl", "Beira Litoral"),
        ("Dl", "Douro Litoral"),
        ("Ex", "Estremadura"),
        ("Mb", "Minho Braga"),
        ("Ri", "Ribatejo"),
        ("Tm", "Trás os Montes"),
        ("Ma", "Madeira*"),
        ("Ac", "Açores*"),
    ]

    CIDADE_CHOICES = [
        ("	Lisboa	", "	Lisboa	"),
        ("	Sintra	", "	Sintra	"),
        ("	VilaNovadeGaia	", "	VilaNovadeGaia	"),
        ("	Corvo	", "	Corvo	"),
    ]

    name = models.CharField('Nome', max_length=50, null=False)
    email = models.EmailField('E-mail', null=False)
    ethnicity = models.CharField(
        'Etnia', max_length=10, choices=ETNIA_CHOICES, null=False)
    status = models.CharField('Status', max_length=10,
                              choices=STATUS_CHOICES, default='Ativo')

    street = models.CharField('Logradouro', max_length=50, null=False)
    number = models.IntegerField('Nº', null=False)
    complement = models.CharField('Complemento', max_length=10, blank=True)
    city = models.CharField('Cidade', max_length=26,
                            choices=CIDADE_CHOICES, null=False)
    state = models.CharField('Província', max_length=26,
                             choices=PROVINCIA_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def get_absolute_url_detail(self):
        return reverse('client:client_detail', args=[self.pk])

    def get_absolute_url_update(self):
        return reverse('client:client_edit', args=[self.pk])

    def get_absolute_url_delete(self):
        return reverse('client:client_delete', args=[self.pk])

    def __str__(self):
        return self.name


class Phone(models.Model):
    celphone = models.CharField('Celular', max_length=14, null=False)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='cliente_telefone')

    def __str__(self):
        return self.celphone


class SocialMedia(models.Model):
    socialmedia = models.CharField('Rede Social', max_length=50)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='cliente_midiasocial')

    def __str__(self):
        return self.socialmedia


class Product(models.Model):

    name = models.CharField('Produto', max_length=255, unique=True)
    slug = AutoSlugField(unique=True, always_update=False,
                         populate_from="name")
    image = models.ImageField(
        'Imagem do produto', upload_to="produtos/%Y", blank=True)
    description = models.TextField('Descrição', blank=True)
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    available = models.BooleanField('Disponível', default=True)
    quantity = models.IntegerField ('Quantidade')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.name


@receiver(post_save, sender=Product)
def insert_slug(sender, instance, **kwargs):
    if not instance.slug or instance.slug != slugify(instance.name):
        instance.slug = slugify(instance.name)
        return instance.save()



class Order(models.Model):

    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Pronto', 'Pronto'),
        ('Aguardando', 'Aguardando'),
        ('Enviado', 'Enviado'),
        ('Entregue', 'Entregue'),
        ('Cancelado', 'Cancelado'),
    ]

    PGTO_CHOICES = [
        ("Pix", "pix"),
        ("Cartão", "cartão"),
        ("Dinheiro", "dinheiro"),
    ]

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='cliente_pedido')
    withdraw = models.BooleanField('Retirar', default=False)
    date = models.DateField('Data de entrega')
    formpayment = models.CharField(
        'Forma pgto', max_length=11, choices=PGTO_CHOICES)
    total = models.DecimalField(
        'Total', max_digits=11, decimal_places=2, default=0, null=True)
    status = models.CharField(
        'Condição', max_length=10, choices=STATUS_CHOICES, default='Pendente')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def get_absolute_url_details(self):
        return reverse('formset:order_details', args=[self.pk])

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
