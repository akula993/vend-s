from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone


class Addres(models.Model):
    PAYMENT = (
        ('nal', "Наличный расчет"),
        ('bez', "Безналичный расчет"),
    )
    name = models.CharField("Адрес", max_length=255)
    slug = models.SlugField('URL', unique=True, blank=True,null=True)
    to_rent = models.DecimalField('Аренда', max_digits=10, decimal_places=2, blank=True, null=True, )
    publish = models.DateTimeField(default=timezone.now, blank=True, null=True, )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment = models.CharField('Оплата', max_length=3, choices=PAYMENT, default='bez')

    def __str__(self):
        return self.name

    def get_sum(self):
        sum_number = Counter.objects.aggregate(total_price=Sum('number'))['total_price']
        n = sum_number * 10
        return n

    def get_sell(self):
        sum_number = Counter.objects.aggregate(total_price=Sum('number'))['total_price']
        sum_rent = self.to_rent
        s = sum_number - sum_rent
        return s

class Device(models.Model):
    address = models.ForeignKey(Addres, on_delete=models.PROTECT, related_name='addres')
    name = models.CharField("Название", blank=True, null=True, max_length=150, default='Кран')

    # def get_absolute_url(self):
    #     return reverse('device', kwargs={'post_id': self.pk, 'slug_address': self.address.slug})
    def __str__(self):
        return f'{self.address.name} | {self.name}'

    def get_absolute_url(self):
        return reverse('address', kwargs={'slug_neme': self.address.slug})
    # def get_absolute_url(self):
    #     return reverse('device', kwargs={'id': self.id, 'name': self.name})

class Counter(models.Model):
    device = models.ForeignKey(Device, on_delete=models.PROTECT, related_name='counter')
    month = models.DateTimeField('Дата снятия счетчика', auto_now=True)
    number = models.IntegerField(verbose_name='Счетчик', default=0)
    expenditure = models.IntegerField(verbose_name='Раход', default=0)
    toys = models.DecimalField('Игрушки', max_digits=10, decimal_places=2, default=0)
    service = models.DecimalField('обслуживание', max_digits=10, decimal_places=2, default=0)
    service_description = models.TextField('обслуживание описание', blank=True, )
    petrol = models.DecimalField('бензин', max_digits=10, decimal_places=2, default=0)
    other = models.DecimalField('прочие', max_digits=10, decimal_places=2, default=0)
    other_description = models.TextField('прочие описание', blank=True)

    def __str__(self):
        return f'{self.device.address} | {self.device.name}'

    def get_absolute_url(self):
        return reverse('home', kwargs={'id': self.id, 'name': self.month})
