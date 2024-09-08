from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import EventDetails,EventGuests,EventTickets
from users.models import BusinessAccount, TeamManager
from taskmanager.models import Task
from django.contrib import messages
# Create your views here.
def  create_event(request):
    if request.method == 'POST':
        b_account = BusinessAccount.objects.get(user=request.user)
        name = request.POST.get('name')
        details = request.POST.get('details')
        location = request.POST.get('location')
        event_cateogry = request.POST.get('event_cateogry')
        date = request.POST.get('event_date')
        time = request.POST.get('event_time')
        event = EventDetails.objects.create(name=name, details=details, location=location, event_date=date, event_time=time, created_by=b_account, event_cateogry=event_cateogry)
        return redirect("view-event", id=event.id)
    return render(request, "events/create-event.html")


def add_guests(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event = EventDetails.objects.get(id=event_id)
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        guest = EventGuests.objects.create(name=name, description=description, image=image, event=event)
        return redirect("view-event", id=event.id)
    return render(request, "home/add-guests.html")


def assign_team(request,event_id):
        account = BusinessAccount.objects.get(user=request.user)
        team = TeamManager.objects.get(user=account)
        event = EventDetails.objects.get(id=event_id)
        event.team = team
        event.save()
        messages.success(request, 'Team assigned successfully')
        return redirect("view-event", id=event.id)

from datetime import datetime, timedelta

def list_team_events(request):
    account = BusinessAccount.objects.get(user=request.user)
    team = TeamManager.objects.get(user=account)
    today = datetime.now().date()
    upcoming_threshold = today + timedelta(days=10)
    events = EventDetails.objects.filter(created_by=account)
    upcoming_events = events.filter(event_date__range=[today, upcoming_threshold])
    return render(request, "events/my-events.html", {'events': events, 'upcoming_events': upcoming_events,"account":account})



def ViewEvent(request, id):
    event = get_object_or_404(EventDetails, id=id)
    account = BusinessAccount.objects.get(user=request.user)
    team = TeamManager.objects.get(user=account)
    tasks = Task.objects.filter(event=event)
    if(tasks.count() >0):
        progress = round(tasks.filter(status="done").count()/tasks.count()*100)
    else:
        progress = 0
    return render(request, "events/event-details.html", {'event':event,"team":team,"tasks":tasks,"progress":progress,"account":account})


def get_events(request):
    if request.method == 'GET':
        month = request.GET.get('month') #11
        month = int(month) #11
        month +=1 #12 
    account = BusinessAccount.objects.get(user=request.user)
    # try:
    events = EventDetails.objects.filter(created_by=account,event_date__month=month)
    return_data = {}
    for x in events:
        if return_data.get(x.event_date.day):
            return_data[x.event_date.day].append({'event_name':x.name,'event_id':x.id,'event_date':x.event_date.strftime("%d %B %Y")})
        else:
            return_data[x.event_date.day]=[{'event_name':x.name,'event_id':x.id,'event_date':x.event_date.strftime("%d %B %Y")}]
    return JsonResponse(return_data)
    # except Exception as e:
    #     print(e)
    #     messages.warning(request, 'Event does not esxist')
    #     return HttpResponse(e)