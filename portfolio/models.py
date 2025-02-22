from decimal import Decimal
import os
import random
from django.contrib.auth import get_user_model

from django.conf import settings
from django.db import models

User = get_user_model()


PORTFOLIO_TITLES = [
        ('Cryptocurrency', 'Cryptocurrency'),
        ('Gold', 'Gold'),
    ]


PORTFOLIO_TYPES = [
        ('Metal', 'Metal'),
        ('Software', 'Software'),
    ]


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    title = models.CharField(max_length=255, choices=PORTFOLIO_TITLES)  # The title of the portfolio
    type = models.CharField(max_length=255, choices=PORTFOLIO_TYPES)  # The title of the portfolio
    image = models.ImageField(upload_to='portfolio/', null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def calculate_total(self):
        # Calculate the total value of all associated content
        total_value = Decimal('0.00')
        for content in self.contents.all():
            total_value += content.calculate_total()
        return total_value

class Content(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='contents', on_delete=models.CASCADE)
    type = models.CharField(max_length=255)  # Type of the asset (Bitcoin, Gold Coins, etc.)
    value = models.CharField(max_length=255)  # Value of the asset (e.g., $28,000)
    quantity = models.IntegerField(null=True, blank=True)  # Quantity of the asset
    total = models.CharField(max_length=255, null=True, blank=True)  # Total value (e.g., $3,452)
    image = models.ImageField(upload_to='contents/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.type} ({self.portfolio.title})"
    

    def calculate_total(self):
        # Convert value to a decimal and calculate the total for this content
        try:
            value = Decimal(self.value.replace('$', '').replace(',', ''))
            total_value = value * self.quantity
            return total_value
        except Exception as e:
            print(f"Error calculating total for content: {e}")
            return Decimal('0.00')

    def save(self, *args, **kwargs):
        # Automatically calculate and update the `total` field before saving
        self.total = str(self.calculate_total())
        super().save(*args, **kwargs)



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