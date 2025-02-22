from django.contrib import admin

from delivery.models import Delivery, DeliveryStatus

admin.site.register(Delivery)
admin.site.register(DeliveryStatus)
