from django.db import models
from django.db.models import Sum, Count, Max
from django.urls import reverse
from django.utils import timezone


class Address(models.Model):
    PAYMENT = (
        ('nal', "Наличный расчет"),
        ('bez', "Безналичный расчет"),
    )
    name = models.CharField("Адрес", max_length=255)
    slug = models.SlugField('URL', unique=True, blank=True, null=True)
    to_rent = models.DecimalField('Аренда', max_digits=10, decimal_places=2, blank=True, null=True, )
    publish = models.DateTimeField(default=timezone.now, blank=True, null=True, )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment = models.CharField('Оплата', max_length=3, choices=PAYMENT, default='bez')

    def __str__(self):
        return self.name

    # def get_all_sum(self):
    #     sum_number = Device.get_sum()

    # s = sum_number.
    # (total_price=Sum('number'))['total_price']
    # n = sum_number * 10
    # return s

    # def get_sell(self):
    #     sum_number = Counter.objects.aggregate(total_price=Sum('number'))['total_price']
    #     # print(sum_number)
    #
    #     # sum_rent = self.to_rent
    #     # print(sum_rent)
    #     # s = sum_number - sum_rent
    #     # print(s)
    #     # return s/

    @classmethod
    def get_default_pk(cls):
        obj, created = cls.objects.get_or_create(name='Без адреса')
        return obj.pk

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def get_sum_all(self):
        address_sum = Address.objects.get(name=self.name)
        a = address_sum.device.all()
        if address_sum.device.all() and not None:
            print(a[1:1])
            for i in a:
                device_sum = a.get(name=self.name)
                print(device_sum, 'Адрес')

                try:
                    last, pre_last = device_sum.sensor_set.order_by('-month')[:2]
                    sum_number = (last.number - pre_last.number) * 10
                except ValueError:
                    try:
                        last, pre_last = device_sum.sensor_set.last(), 0
                        sum_number = (last.number) * 10
                    except AttributeError:
                        sum_number = 0
            sum_number = 0
        else:
            print('Нет нечего')
            sum_number =0
        return sum_number


class Device(models.Model):
    address = models.ForeignKey(Address, on_delete=models.SET_DEFAULT, related_name='device',
                                default=Address.get_default_pk, verbose_name="Адреса")
    name = models.CharField("Название", blank=True, max_length=150, default='')

    def get_sum(self):
        device_sum = Device.objects.get(name=self.name)
        # last, pre_last = device_sum.sensor_set.order_by('-month')[:2]
        # # sum_number = device_sum.sensor.aggregate(total_price=Max('number', ))['total_price']
        # sum_number = (last.number - pre_last.number) * 10
        try:
            last, pre_last = device_sum.sensor_set.order_by('-month')[:2]
            sum_number = (last.number - pre_last.number) * 10
        except ValueError:
            try:
                last, pre_last = device_sum.sensor_set.last(), 0
                sum_number = (last.number) * 10
            except AttributeError:
                sum_number = 0
        return sum_number

    def get_sell(self):
        device_sum = Device.objects.get(name=self.name)
        try:
            last, pre_last = device_sum.sensor_set.order_by('-month')[:2]
            sum = (last.number - pre_last.number) * 10
        except ValueError:
            try:
                last, pre_last = device_sum.sensor_set.last(), 0
                sum = (last.number) * 10
            except AttributeError:
                sum = 0
        sum_number = sum - self.address.to_rent
        return sum_number

    # def get_absolute_url(self):
    #     return reverse('device', kwargs={'post_id': self.pk, 'slug_address': self.address.slug})
    def __str__(self):
        return f'{self.address.name} | {self.name}'

    # queryset = (
    #     Counter
    #     .objects
    #     .values('category__name')
    #     .annotate(name=F('category__name'))
    #     .annotate(cnt=Count('id'))
    #     .order_by('category__name')
    #     .values('name', 'cnt')
    # )



    class Meta:
        verbose_name = 'Аппарат'
        verbose_name_plural = 'Аппараты'

    def get_absolute_url(self):
        return reverse('address', kwargs={'slug_name': self.address.slug})


class Sensor(models.Model):
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    month = models.DateTimeField('Дата снятия счетчика', auto_now=True)
    number = models.IntegerField(verbose_name='Счетчик', default=0)
    def get_sum(self):
        sum_number = Device.objects.aggregate(total_price=Count('counter'))['total_price']
        n = sum_number * 10
        return n
    def __str__(self):
        return f'{self.device.address} | {self.device.name}'

    def get_absolute_url(self):
        return reverse('home', kwargs={'id': self.id, 'name': self.month})

    class Meta:
        verbose_name = 'Счетчик'
        verbose_name_plural = 'Счетчики'


class Expenditure(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='expenditure', verbose_name='Аппарат')
    toys = models.DecimalField('Игрушки', max_digits=10, decimal_places=2, default=0)
    petrol = models.DecimalField('бензин', max_digits=10, decimal_places=2, default=0)
    service = models.DecimalField('обслуживание', max_digits=10, decimal_places=2, default=0)
    service_description = models.TextField('обслуживание описание', blank=True, )

    class Meta:
        verbose_name = 'Раход'
        verbose_name_plural = 'Раходы'

    def __str__(self):
        return f'Аппарат: {self.device.name} | Игрушки: {self.toys} | бензин: {self.toys} | обслуживание: {self.toys}'


class AddOptions(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='addoptions')

    other = models.DecimalField('прочие', max_digits=10, decimal_places=2, default=0)
    other_description = models.TextField('прочие описание', blank=True)

    class Meta:
        verbose_name = 'Дополнительная опции'
        verbose_name_plural = 'Дополнительные опции'

    def __str__(self):
        return self.device.name
