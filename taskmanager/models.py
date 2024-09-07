from django.db import models

# Create your models here.

choices = (("todo","todo"), ("progress","progress"), ("review","review"), ("done","done"))
priority_choices = (("low","low"), ("medium","medium"), ("high","high"))



class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    priority = models.CharField(max_length=100,choices=priority_choices,default="low")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    team = models.ForeignKey("users.TeamManager", on_delete=models.CASCADE)
    status = models.CharField(max_length=100,choices=choices,default="todo")
    assigned_to = models.ManyToManyField("users.TeamMember", related_name="assigned_tasks")
    def __str__(self):
        return self.title
    
class TodoList(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    team = models.ForeignKey("users.TeamManager", on_delete=models.CASCADE,null=True, blank=True)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey("users.TeamMember", on_delete=models.CASCADE,null=True, blank=True)
    todo_items = models.ManyToManyField("TodoItem", related_name="todo_list")
    task = models.ForeignKey("Task", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
    
class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title