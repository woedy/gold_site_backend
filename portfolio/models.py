import os
import random

from django.conf import settings
from django.db import models



class Portfolio(models.Model):
    title = models.CharField(max_length=255)  # The title of the portfolio
    image = models.URLField()  # URL to the image for the portfolio
    
    def __str__(self):
        return self.title


class Content(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='content', on_delete=models.CASCADE)
    type = models.CharField(max_length=255)  # Type of the asset (Bitcoin, Gold Coins, etc.)
    value = models.CharField(max_length=255)  # Value of the asset (e.g., $28,000)
    quantity = models.IntegerField()  # Quantity of the asset
    total = models.CharField(max_length=255)  # Total value (e.g., $3,452)
    image = models.URLField()  # URL to the image for the content
    
    def __str__(self):
        return f"{self.type} ({self.portfolio.title})"






class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    price_per_unit = models.DecimalField(max_digits=18, decimal_places=8)
    total_value = models.DecimalField(max_digits=18, decimal_places=8)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} {self.asset.symbol} for {self.total_value}"


class PriceHistory(models.Model):
#    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=18, decimal_places=8)  # Price of the asset at that time
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.asset.name} - {self.price} at {self.timestamp}"

    @classmethod
    def get_latest_price(cls, asset):
        latest = cls.objects.filter(asset=asset).order_by('-timestamp').first()
        return latest.price if latest else Decimal('0')


class BitcoinPrice(models.Model):
    # You can store the latest Bitcoin price in a separate model or integrate with an external API
    price = models.DecimalField(max_digits=18, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_latest_bitcoin_price(cls):
        latest = cls.objects.order_by('-timestamp').first()
        return latest.price if latest else Decimal('0')