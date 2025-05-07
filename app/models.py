from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class SellerDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    brand_name = models.CharField(max_length=25, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    bank_name= models.CharField(max_length=50,null=True, blank=True)
    account_number = models.CharField(max_length=10, null=True, blank=True)
    balance = models.BigIntegerField(null=True, blank=True, default=0)
    def __str__(self):
        return f"{self.user.username}"