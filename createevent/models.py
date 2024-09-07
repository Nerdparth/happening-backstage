from django.db import models

# Create your models here.
class EventDetails(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    details = models.CharField(max_length=2000, null=False, blank=False)
    price = models.IntegerField(max_length=10)
    guests = models.CharField(max_length=50)

