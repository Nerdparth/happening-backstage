from django.shortcuts import render
from users.models import BusinessAccount, TeamManager, TeamMember
from taskmanager.models import Task
from django.utils import timezone
from createevent.models import EventDetails
from .models import Meetings, Whiteboard
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def dashboard(request):
    account = BusinessAccount.objects.get(user=request.user)
    team = TeamManager.objects.get(user=account)
    tasks = Task.objects.filter(team=team).exclude(status="done").order_by('end_date')

    priority_tasks = Task.objects.filter(team=team,priority="high").count()
    priority_tasks_complete = Task.objects.filter(team=team,priority="high",status="done").count()
    meetings = Meetings.objects.filter(team=team)
    whiteboards = Whiteboard.objects.filter(created_by=account)
    pending_tasks = Task.objects.filter(team=team).exclude(status="done").count()
    overdue_tasks = Task.objects.filter(team=team, end_date__lt=timezone.now()).exclude(status="done").count()
    upcoming_events = EventDetails.objects.filter(created_by=account).filter(event_date__gt=timezone.now())
    return render(request, 'home/dashboard.html',context={'account':account,'team':team,"tasks":tasks,"priority_tasks":priority_tasks,"priority_tasks_complete":priority_tasks_complete,"pending_tasks":pending_tasks,"overdue_tasks":overdue_tasks,"meetings":meetings,"whiteboards":whiteboards,"events":upcoming_events})

def calendar_view(request):
    account = BusinessAccount.objects.get(user=request.user)
    team = TeamManager.objects.get(user=account)
    events = EventDetails.objects.filter(created_by=account)
    return render(request, 'home/calendar-view.html', {'events': events, "account":account})



@csrf_exempt
def create_meeting(request):
    account = BusinessAccount.objects.get(user=request.user)
    team = TeamManager.objects.get(user=account)
    if request.method == 'POST':
        meet_id = request.POST.get('meet_id')
        team = TeamManager.objects.get(user=account)
        meeting = Meetings.objects.create(meet_id=meet_id, meet_title=meet_id, team=team)
        return JsonResponse({"success":True})
    return JsonResponse({"success":False})


@csrf_exempt
def create_whiteboard(request):
    account = BusinessAccount.objects.get(user=request.user)
    team = TeamManager.objects.get(user=account)
    if request.method == 'POST':
        board_id = request.POST.get('board_id')
        whiteboard = Whiteboard.objects.create(board_id=board_id, created_by=account)
        return JsonResponse({"success":True})
    return JsonResponse({"success":False})
    