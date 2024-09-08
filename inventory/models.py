from django.db import models

# Create your models here.
class InventoryItem(models.Model):
    itemName = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    quantity = models.IntegerField()
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.ForeignKey("Inventory", on_delete=models.CASCADE)

    def __str__(self):
        return self.itemName
    
class Inventory(models.Model):
    account = models.ForeignKey("users.BusinessAccount", on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    spent = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
        return self.account.user.username