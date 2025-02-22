from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save

from gold_site_pro.utils import unique_tracking_number_generator
from portfolio.models import Content
User = get_user_model()


class Delivery(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    assets = models.ManyToManyField(Content, related_name='assets', blank=True)



    location_name = models.CharField(max_length=5000, null=True, blank=True)
    lat = models.DecimalField(default=0.0, max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(default=0.0, max_digits=30, decimal_places=15, null=True, blank=True)
    

    
    billing_address_1 = models.TextField(null=True, blank=True)
    billing_address_2 = models.TextField(null=True, blank=True)
    billing_address_3 = models.TextField(null=True, blank=True)

    
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    payment_option = models.CharField(max_length=20, choices=[('Bitcoin', 'Bitcoin'), ('Credit Card', 'Credit Card'), ('Bank Transfer', 'Bank Transfer')], default='Bitcoin')

    is_draft = models.BooleanField(default=True)

    tracking_number = models.CharField(max_length=100, null=True, blank=True)

    
    delivery_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Initiated', 'Initiated'), ('Packed', 'Packed'), ('In Transit', 'In Transit'), ('Delivered', 'Delivered')], default='Pending')
    estimated_delivery_date = models.DateTimeField(null=True, blank=True)
    actual_delivery_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Delivery for - Status: {self.delivery_status}"
    


def pre_save_tracking_number_receiver(sender, instance, *args, **kwargs):
    if not instance.tracking_number:
        instance.tracking_number = unique_tracking_number_generator(instance)

pre_save.connect(pre_save_tracking_number_receiver, sender=Delivery)









class DeliveryStatus(models.Model):

    
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=20, choices=[('Initiated', 'Initiated'), ('Packed', 'Packed'), ('In Transit', 'In Transit'), ('Delivered', 'Delivered')], default='Initiated')
    sub_status = models.CharField(max_length=500)
    active = models.BooleanField(default=False)

