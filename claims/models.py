from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Claim(models.Model):
    STATUS_CHOICES = [
        ('No Claim', 'No Claim'),
        ('Pending', 'Pending'),
        ('verified', 'Verified'),
        ('Paid', 'Paid'),
        ('Completed', 'Completed'),
    ]

    client = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='No Claim')
    claim_date = models.DateTimeField(auto_now_add=True)
    verification_date = models.DateTimeField(null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    claim_ref = models.CharField(max_length=255) 
    security_question_1 = models.CharField(max_length=1000) 
    security_answer_1 = models.CharField(max_length=1000) 
    security_question_2 = models.CharField(max_length=1000) 
    security_answer_2 = models.CharField(max_length=1000) 

    bitcoin_qr = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    bitcoin_address = models.ImageField(upload_to='qr_codes/', null=True, blank=True)


    def __str__(self):
        return f"Claim by {self.client.first_name} - Status: {self.status}"
