from sheep.models import Device, Flock, Sheep

from django.contrib import admin

DEVICE_FIELDS = (
    'uuid',
    'comment'
)


class DeviceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': DEVICE_FIELDS}),
    )
    list_display = DEVICE_FIELDS
    search_fields = DEVICE_FIELDS
    ordering = ('created',)

admin.site.register(Device, DeviceAdmin)


FLOCK_FIELDS = (
    'flock_id',
    'phone_number',
    'comment',
    'alert'
)


class FlockAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': FLOCK_FIELDS}),
    )
    list_display = FLOCK_FIELDS
    search_fields = FLOCK_FIELDS
    ordering = ('created',)

admin.site.register(Flock, FlockAdmin)


SHEEP_FIELDS = (
    'flock',
    'sheep_id',
    'comment',
    'alert'
)


class SheepAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': SHEEP_FIELDS}),
    )
    list_display = SHEEP_FIELDS
    search_fields = SHEEP_FIELDS
    ordering = ('created',)

admin.site.register(Sheep, SheepAdmin)
