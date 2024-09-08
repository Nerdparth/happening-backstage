from django.contrib import admin
from .models import InventoryItem,Inventory  # Ensure this import is correct

# Register your models here.
admin.site.register(InventoryItem)
admin.site.register(Inventory)

