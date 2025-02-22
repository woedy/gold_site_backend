from django.db import models
from django.contrib.auth import get_user_model

from portfolio.models import Content
User = get_user_model()
class Delivery(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    assets = models.ManyToManyField(Content, related_name='assets')



    location_name = models.CharField(max_length=5000, null=True, blank=True)
    lat = models.DecimalField(default=0.0, max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(default=0.0, max_digits=30, decimal_places=15, null=True, blank=True)
    

    
    billing_address_1 = models.TextField()
    billing_address_2 = models.TextField()
    billing_address_3 = models.TextField()

    
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    payment_option = models.CharField(max_length=20, choices=[('Bitcoin', 'Bitcoin'), ('Credit Card', 'Credit Card'), ('Bank Transfer', 'Bank Transfer')], default='pending')

    is_draft = models.BooleanField(default=True)

    tracking_number = models.CharField(max_length=100, null=True, blank=True)

    
    delivery_status = models.CharField(max_length=20, choices=[('Initiated', 'Initiated'), ('Packed', 'Packed'), ('In Transit', 'In Transit'), ('Delivered', 'Delivered')], default='Initiated')
    estimated_delivery_date = models.DateTimeField(null=True, blank=True)
    actual_delivery_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Delivery for Claim {self.claim.id} - Status: {self.delivery_status}"
    







class DeliveryStatus(models.Model):

    
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=20, choices=[('Initiated', 'Initiated'), ('Packed', 'Packed'), ('In Transit', 'In Transit'), ('Delivered', 'Delivered')], default='Initiated')
    sub_status = models.CharField(max_length=500)
    active = models.BooleanField(default=False)

