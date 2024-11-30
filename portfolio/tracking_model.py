from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class GoldAsset(models.Model):
    name = models.CharField(max_length=50)
    weight_in_grams = models.DecimalField(max_digits=18, decimal_places=2)
    purity = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 99.99 for pure gold
    serial_number = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"

class Claim(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    gold_asset = models.ForeignKey(GoldAsset, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    claim_date = models.DateTimeField(auto_now_add=True)
    verification_date = models.DateTimeField(null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    shipment_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Claim for {self.gold_asset.name} by {self.client.username} - Status: {self.status}"

class Payment(models.Model):
    claim = models.OneToOneField(Claim, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=18, decimal_places=2)  # Total payment amount
    payment_method = models.CharField(max_length=50)  # E.g., Credit Card, Bank Transfer
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Claim {self.claim.id} - Amount: {self.amount} - Status: {self.payment_status}"

class Courier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=200)
    tracking_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class Delivery(models.Model):
    claim = models.OneToOneField(Claim, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    delivery_address = models.TextField()
    delivery_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('in_transit', 'In Transit'), ('delivered', 'Delivered')], default='pending')
    estimated_delivery_date = models.DateTimeField(null=True, blank=True)
    actual_delivery_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Delivery for Claim {self.claim.id} - Status: {self.delivery_status}"

class DeliveryConfirmation(models.Model):
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE)
    client_signature = models.ImageField(upload_to='signatures/', null=True, blank=True)  # For client to sign receipt
    received_by = models.CharField(max_length=100)  # Name of person receiving the gold
    confirmation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery Confirmation for Claim {self.delivery.claim.id}"
