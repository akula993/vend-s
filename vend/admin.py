from django.contrib import admin

from vend.models import Device, Address, Sensor, Expenditure, AddOptions, Sensor_win


class De(admin.TabularInline):
    model = Device
class Se(admin.TabularInline):
    model = Sensor
    extra = 0
class Se_win(admin.TabularInline):
    model = Sensor_win
    extra = 0


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    # exclude = ('slug',)
    inlines = [De,]
    prepopulated_fields = {'slug': ('name',)}
    # readonly_fields = ('slug',)
    save_as = True

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    save_as = True


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    save_as = True
    inlines = [Se, Se_win]

@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    save_as = True

@admin.register(AddOptions)
class AddOptionsAdmin(admin.ModelAdmin):
    save_as = True
