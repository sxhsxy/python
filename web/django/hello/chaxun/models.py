from django.db import models

# Create your models here.


class AccountInfo(models.Model):
    identify_number = models.CharField(max_length=18, unique=True)
    full_name = models.CharField(max_length=64)
    account_number = models.CharField(max_length=64)
    salary = models.DecimalField(max_digits=10, decimal_places=2)


