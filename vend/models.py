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
    slug = models.SlugField('URL', max_length=255, unique=True, blank=True, null=True)
    to_rent = models.DecimalField('Аренда', max_digits=10, decimal_places=2, blank=True, null=True, )
    publish = models.DateTimeField(default=timezone.now, blank=True, null=True, )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment = models.CharField('Оплата', max_length=3, choices=PAYMENT, default='bez')

    def get_absolute_url(self):
        return reverse('address', kwargs={'slug': self.slug})
    def __str__(self):
        return self.name


    @classmethod
    def get_default_pk(cls):
        obj, created = cls.objects.get_or_create(name='Без адреса')
        return obj.pk

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def get_sum_all(self):
        address_sum = Address.objects.get(name=self.name)
        device_sum = address_sum.device.all()
        def item(aa=0, *args):
                sum_number = []

                for i in args:
                    for a in i:
                        for s in a:
                            sum_number.append(s.number)

                return sum(sum_number)
        if device_sum and not None:

            sum_number_list = []
            for dev_sum in device_sum:
                current_datetime = timezone.now()
                list_date = dev_sum.sensor_set.filter(month__year=current_datetime.year,
                                                      month__month=current_datetime.month)
                sum_number_list.append(list_date)
            sum_number = item(0, sum_number_list) * 10

        else:
            sum_number = 0
        return sum_number

    def get_sum_all_sell(self):
        address_sum = Address.objects.get(name=self.name)
        device_sum = address_sum.device.all()
        def item(aa=0, *args):
                sum_number = []

                for i in args:
                    for a in i:
                        for s in a:
                            sum_number.append(s.number)

                return sum(sum_number)
        if device_sum and not None:

            sum_number_list = []
            for dev_sum in device_sum:
                current_datetime = timezone.now()
                list_date = dev_sum.sensor_set.filter(month__year=current_datetime.year,
                                                      month__month=current_datetime.month)
                sum_number_list.append(list_date)
            sum_number = item(0, sum_number_list)
            sum_number =sum_number * 10 -self.to_rent

        else:
            sum_number = 0
        return sum_number


class Device(models.Model):
    address = models.ForeignKey(Address, on_delete=models.SET_DEFAULT, related_name='device',
                                default=Address.get_default_pk, verbose_name="Адреса")
    name = models.CharField("Название", blank=True, max_length=150, default='')
    def get_sum(self):
        device_sum = Device.objects.get(name=self.name)
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
    def get_sum_win(self):
        device_sum = Device.objects.get(name=self.name)
        try:
            last, pre_last = device_sum.sensor_win_set.order_by('-month')[:2]
            sum_number = (last.number - pre_last.number)
        except ValueError:
            try:
                last, pre_last = device_sum.sensor_win_set.last(), 0
                sum_number = (last.number)
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
    def __str__(self):
        return f'{self.address.name} | {self.name}'
    class Meta:
        verbose_name = 'Аппарат'
        verbose_name_plural = 'Аппараты'

    def get_absolute_url(self):
        return reverse('device', kwargs={'device_id': self.pk})


class Sensor(models.Model):
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    month = models.DateTimeField('Дата снятия счетчика', auto_now_add=True)
    number = models.IntegerField(verbose_name='Счетчик', default=0)

    def get_sum(self):
        sum_number = Device.objects.aggregate(total_price=Count('counter'))['total_price']
        n = sum_number * 10
        return n

    def multiply(self):
        return self.number * 10
    def __str__(self):
        return f'{self.device.address} | {self.device.name}'

    # def get_absolute_url(self):
    #     return reverse('home', kwargs={'id': self.id})

    class Meta:
        verbose_name = 'Счетчик игр'
        verbose_name_plural = 'Счетчики игры'
class Sensor_win(models.Model):
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    month = models.DateTimeField('Дата снятия счетчика', default=timezone.now())
    number = models.IntegerField(verbose_name='Счетчик', default=0)

    def __str__(self):
        return f'{self.device.address} | {self.device.name}'

    class Meta:
        verbose_name = 'Счетчик выигрыша'
        verbose_name_plural = 'Счетчики выигрешей'


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
