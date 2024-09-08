from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("calendar-view", views.calendar_view, name="calendar-view"),
    path("create-meeting", views.create_meeting, name="create-meeting"),
    path("create-whiteboard", views.create_whiteboard, name="create-whiteboard"),
    path("teams", views.teams_page, name="teams"),
    path("accounts", views.accounts_page, name="accounts"),

]
