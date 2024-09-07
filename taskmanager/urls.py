from django.urls import path
from . import views


urlpatterns = [
    path('task/create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.view_task, name='view_task'),
    path('task/<int:task_id>/update/', views.update_task, name='update_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/change_status/', views.change_task_status, name='change_task_status'),
    path('tasks/', views.get_team_tasks, name='get_team_tasks'),
    path("todo-list/create/", views.create_todo_list, name="create_todo_list"),
    path("todo-list/add-item/", views.create_todo_item, name="add_todo_item"),
    path("todo-list/complete-item/<int:item_id>", views.complete_todo_item, name="complete_todo_item"),

]