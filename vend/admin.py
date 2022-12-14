from django.contrib import admin

from vend.models import Device, Address, Sensor, Expenditure, AddOptions


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    # exclude = ('slug',)

    prepopulated_fields = {'slug': ('name',)}
    # readonly_fields = ('slug',)
    save_as = True

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    save_as = True


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    save_as = True

@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    save_as = True

@admin.register(AddOptions)
class AddOptionsAdmin(admin.ModelAdmin):
    save_as = True
