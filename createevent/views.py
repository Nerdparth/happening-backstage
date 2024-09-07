from django.shortcuts import render, redirect, get_object_or_404
from .models import EventDetails

# Create your views here.
def  CreateEvent(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        details = request.POST.get('details')
        price = request.POST.get('price')
        guests = request.POST.get('guests')
        new_event = EventDetails.objects.create(name=name,details=details, price=price, guests=guests)
        return redirect("view-event", id=new_event.id)
    return render(request, "home/create-event.html")

def ViewEvent(request, id):
    event = get_object_or_404(EventDetails, id=id)
    return render(request, "home/view-event.html", {'event':event})