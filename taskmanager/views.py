from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from users.models import BusinessAccount, TeamManager, TeamMember
from .models import Task, TodoList, TodoItem
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from createevent.models import EventDetails
import requests


def taskmanager_home(request):
    account = BusinessAccount.objects.get(user=request.user)
    team = TeamManager.objects.get(user=account)
    tasks = Task.objects.filter(team=team).exclude(status="done").order_by('end_date')

    priority_tasks = Task.objects.filter(team=team,priority="high").count()
    priority_tasks_complete = Task.objects.filter(team=team,priority="high",status="done").count()

    pending_tasks = Task.objects.filter(team=team).exclude(status="done").count()
    overdue_tasks = Task.objects.filter(team=team, end_date__lt=timezone.now()).exclude(status="done").count()

    return render(request, 'taskmanager/taskmanager.html',context={'account':account,'team':team,"tasks":tasks,"priority_tasks":priority_tasks,"priority_tasks_complete":priority_tasks_complete,"pending_tasks":pending_tasks,"overdue_tasks":overdue_tasks})





def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        event = request.POST.get('event_id')
        description = request.POST.get('description')
        team_id = request.POST.get('team_id')
        priority = request.POST.get('priority')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')
        team = TeamManager.objects.get(team_id=team_id)
        event = EventDetails.objects.filter(id=event)
        if event:
            event = event[0]
        else:
            event = None
        task = Task.objects.create(title=title, description=description, team=team, priority=priority, start_date=start_date, end_date=end_date, status=status,event=event)
        return HttpResponseRedirect('/taskmanager/task/'+str(task.id))


def view_task(request, task_id):
    task = Task.objects.get(id=task_id)
    todo_lists = TodoList.objects.filter(task=task)
    account = BusinessAccount.objects.get(user=request.user)
    team = TeamManager.objects.get(user=account)
    tasks = Task.objects.filter(team=team).exclude(status="done").order_by('end_date')

    return render(request, 'taskmanager/task.html', {'task':task,"todos":todo_lists, "account":account,"team":task.team,"tasks":tasks})  

def update_task(request, task_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        task = Task.objects.get(id=task_id)
        task.title = title
        task.description = description
        task.status = status
        task.save()
        return HttpResponseRedirect('/taskmanager/task/'+str(task.id))

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return HttpResponseRedirect('/taskmanager/tasks')

@csrf_exempt
def change_task_status(request, task_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        print(status)
        completed = request.POST.get('completed') == 'on' or False
        task = Task.objects.get(id=task_id)
        task.completed = completed
        task.status = status
        print(task.status)
        task.save()
        print(task.status)
        return render(request, 'taskmanager/task_status.html', {'task':task})

def get_team_tasks(request):
    user = request.user
    b_account = BusinessAccount.objects.get(user=user)
    team_manager = TeamManager.objects.get(user=b_account)
    tasks = Task.objects.filter(team=team_manager)
    return_list = []
    for task in tasks:
        return_list.append({'title':task.title, 'description':task.description, 'status':task.status, 'completed':task.completed,"priority":task.priority,"end_date":task.end_date.strftime("%b %d ")  , 'id':task.id,'assigned_to':[{"email":person.email,"name":person.user} for person in task.assigned_to.all()]})
    return JsonResponse(return_list, safe=False)

def get_team_tasks_month(request):
    user = request.user
    month = request.GET.get('month')
    month = int(month) #11
    month +=1 #12 
    b_account = BusinessAccount.objects.get(user=user)
    team_manager = TeamManager.objects.get(user=b_account)
    tasks = Task.objects.filter(team=team_manager,end_date__month=month)
    return_data = {}    
    for x in tasks:
            if return_data.get(x.start_date.day):
                return_data[x.start_date.day].append({'event_name':x.title,'event_id':x.id,'event_date':x.start_date.strftime("%d %B %Y"),"priority":x.priority})
            else:
                return_data[x.start_date.day]=[{'event_name':x.title,'event_id':x.id,'event_date':x.start_date.strftime("%d %B %Y"),"priority":x.priority}]
    return JsonResponse(return_data)
    

def get_event_tasks(request,event_id):
    user = request.user
    event = EventDetails.objects.get(id=event_id)
    b_account = BusinessAccount.objects.get(user=user)
    team_manager = TeamManager.objects.get(user=b_account)
    tasks = Task.objects.filter(event=event)
    return_list = []
    for task in tasks:
        return_list.append({'title':task.title, 'description':task.description, 'status':task.status, 'completed':task.completed,"priority":task.priority,"end_date":task.end_date.strftime("%b %d ")  , 'id':task.id,'assigned_to':[{"email":person.email,"name":person.user} for person in task.assigned_to.all()]})
    return JsonResponse(return_list, safe=False)

@csrf_exempt
def create_todo_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        team_id = request.POST.get('team')
        task_id = request.POST.get('task')
        is_private = request.POST.get('is_private') == 'on' or False
        created_by = request.POST.get('created_by')
        team = TeamManager.objects.get(team_id=team_id)
        created_by_user=None
        task=None
        if is_private:
            created_by_user = TeamMember.objects.get(user=created_by)
        else:
            task = Task.objects.get(id=task_id)
        todo_list = TodoList.objects.create(title=title, description=description, team=team, is_private=is_private, created_by=created_by_user,task=task)
        if task:
            lists = TodoList.objects.filter(task=task)
        else:
            lists = TodoList.objects.filter(team=team)
        print("saved and rendered")
        return render(request, 'taskmanager/todo_list_parent.html', {'todos':lists})
    
def create_todo_item(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        todo_list = TodoList.objects.get(id=request.POST.get('todo_list'))
        todo_item = TodoItem.objects.create(title=title, description=description)
        todo_list.todo_items.add(todo_item)
        return render(request, 'taskmanager/todo_list.html', {'todo':todo_list})
    

@csrf_exempt
def complete_todo_item(request, item_id):
    todo_list = TodoList.objects.get(todo_items__id=item_id)
    todo_item = TodoItem.objects.get(id=item_id)
    todo_item.completed = False if todo_item.completed == True else True
    todo_item.save()
    return render(request, 'taskmanager/todo_list.html', {'todo':todo_list})



def assign_task_to_teammate(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        person = TeamMember.objects.get(id=request.POST.get('person_id'))
        task.assigned_to.add(person)
        post_to_external_api(email=person.email,template="mention",subject="Someone Mentioned You",url=f"/taskmanager/tasks/{task_id}",name=person.user,company_name=person.team.user.business_name,msg="")  
        task.save()
        return render(request, 'taskmanager/assign_tasks.html', {'task':task})
    
@csrf_exempt
def remove_task_from_teammate(request,task_id,person_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        person = TeamMember.objects.get(id=person_id)
        task.assigned_to.remove(person)
        task.save()
        return render(request, 'taskmanager/assign_tasks.html', {'task':task})
    

def task_timeline(request):
    account = BusinessAccount.objects.get(user=request.user)
    team = TeamManager.objects.get(user=account)
    tasks = Task.objects.filter(team=team).order_by('end_date')
    return render(request, 'taskmanager/task_timeline.html',context={'account':account,'team':team,"tasks":tasks})

def task_board(request):
    account = BusinessAccount.objects.get(user=request.user)
    team = TeamManager.objects.get(user=account)
    tasks = Task.objects.filter(team=team).order_by('end_date')
    return render(request, 'home/board.html',context={'account':account,'team':team,"tasks":tasks})


def post_to_external_api(email,template,subject,url,name,company_name,msg):
    url = "https://d335-112-196-112-74.ngrok-free.app/api/process-data/"
    payload = {
        "email": email,
        "template": template,
        "subject": subject,
        "url":url,
        "name":name,
        "company_name":company_name,
        "msg": msg
    }
    response = requests.post(url, json=payload)
    print(response)
    return response.status_code