from django.shortcuts import render
from users.models import BusinessAccount, TeamManager, TeamMember
from taskmanager.models import Task
from django.utils import timezone
# Create your views here.
def dashboard(request):
    account = BusinessAccount.objects.get(user=request.user)
    team = TeamManager.objects.get(user=account)
    tasks = Task.objects.filter(team=team).exclude(status="done").order_by('end_date')

    priority_tasks = Task.objects.filter(team=team,priority="high").count()
    priority_tasks_complete = Task.objects.filter(team=team,priority="high",status="done").count()

    pending_tasks = Task.objects.filter(team=team).exclude(status="done").count()
    overdue_tasks = Task.objects.filter(team=team, end_date__lt=timezone.now()).exclude(status="done").count()

    return render(request, 'home/dashboard.html',context={'account':account,'team':team,"tasks":tasks,"priority_tasks":priority_tasks,"priority_tasks_complete":priority_tasks_complete,"pending_tasks":pending_tasks,"overdue_tasks":overdue_tasks})