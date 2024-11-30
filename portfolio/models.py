import os
import random

from django.conf import settings
from django.db import models



class Asset(models.Model):
    ASSET_TYPES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('platinum', 'Platinum'),
        ('palladium', 'Palladium'),
        ('bitcoin', 'Bitcoin'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=ASSET_TYPES)
    symbol = models.CharField(max_length=10)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    



class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Portfolio"
    






class PortfolioItem(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='items')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)  # for precision, especially for Bitcoin
    average_purchase_price = models.DecimalField(max_digits=18, decimal_places=8)  # The average price at which it was purchased
    
    def __str__(self):
        return f"{self.asset.name} - {self.quantity} units"

    @property
    def current_value(self):
        # This would need to get the current price of the asset (implement that logic)
        current_price = self.asset.latest_price()
        return current_price * self.quantity






class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    price_per_unit = models.DecimalField(max_digits=18, decimal_places=8)
    total_value = models.DecimalField(max_digits=18, decimal_places=8)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} {self.asset.symbol} for {self.total_value}"


class PriceHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
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