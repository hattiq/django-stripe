from django.db import models
from django.conf import settings
# Create your models here.

class UserPaymentInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_cus_id = models.CharField(max_length=64)