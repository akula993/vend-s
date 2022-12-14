from django.contrib import admin

from vend.models import Device, Addres, Counter


@admin.register(Addres)
class AddresAdmin(admin.ModelAdmin):
    # exclude = ('slug',)

    prepopulated_fields = {'slug': ('name',)}
    # readonly_fields = ('slug',)
    save_as = True

@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    save_as = True


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    save_as = True
