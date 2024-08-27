from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aadhar_number = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    address = models.TextField()
    balance = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    account_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.user.username} - {self.account_number}'

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    )
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.transaction_type} of {self.amount} on {self.timestamp}'
