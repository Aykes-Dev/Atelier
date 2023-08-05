from django.contrib import admin

from .models import ServicePrice, Bot


class ServicePriceAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'ot', 'price', 'sort_position',
    )


class BotAdmin(admin.ModelAdmin):
    list_display = ('username', 'token', 'active')


admin.site.register(ServicePrice, ServicePriceAdmin)
admin.site.register(Bot, BotAdmin)
