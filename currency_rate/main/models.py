from django.db import models
from django.conf import settings

class Rates(models.Model):
    date = models.DateField(null=False, unique=True)
    base = models.CharField(max_length=3, default="USD")
    currency = models.TextField(max_length=3, default="EUR")
    rate = models.DecimalField(null=False, decimal_places=6, max_digits=10)

