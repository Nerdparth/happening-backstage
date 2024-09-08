from django.urls import path
from .views import inventory, view_inventory, add_budget

urlpatterns = [
    path('add/',inventory, name='add_inventory_item'),
    path('add-money/',add_budget, name='add_money'),

    path('view-inventory', view_inventory, name='view_inventory')
]
