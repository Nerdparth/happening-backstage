from django.shortcuts import render,redirect
from .models import InventoryItem,Inventory
from decimal import Decimal
from users.models import BusinessAccount

def view_inventory(request):
    account = BusinessAccount.objects.get(user=request.user)
    inventory = Inventory.objects.get(account=account)
    items = InventoryItem.objects.all()
    total_items = items.count()
    total_price = sum(item.price for item in items)
    remaining_budget = inventory.budget - inventory.spent
     # Calculate remaining budget

    return render(request, "inventory/inventory.html", {
        'account': account,
        'items': items,
        'inventory': inventory,
        'total_items': total_items,
        'total_price': total_price,
        'remaining_budget': remaining_budget  # Pass this to the template
    })


def add_budget(request):
    if request.method == 'POST':
        account = BusinessAccount.objects.get(user=request.user)
        budget = Decimal(request.POST.get('budget'))  # Convert budget to Decimal
        inv = Inventory.objects.get(
            account=account,
        )
        inv.budget+=budget
        inv.save()
        return redirect('view_inventory')

    return render(request, "inventory/budget-form.html")


def inventory(request):
    if request.method == 'POST':
        price = Decimal(request.POST.get('price'))  # Convert price to Decimal
        inv = Inventory.objects.get(
            account=BusinessAccount.objects.get(user=request.user),
        )
        total_price = inv.spent + price
        # Check if adding the new item would exceed the budget
        if total_price <= inv.budget:  # Ensure you're comparing with Decimal
            itemName = request.POST.get('itemName')
            venue = request.POST.get('venue')
            quantity = request.POST.get('quantity')
            date = request.POST.get('date')
            price = price*int(quantity)
            inv.spent += price
            inv.save()
            InventoryItem.objects.create(
                itemName=itemName,
                venue=venue,
                quantity=quantity,
                date=date,
                price=price,
                inventory=inv,
            )
            return redirect('view_inventory')





