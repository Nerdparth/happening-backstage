from django.urls import path
from . import views

urlpatterns = [
    path("view-event/<int:id>", views.ViewEvent, name='view-event'),
    path("create-event", views.create_event, name='create-event'),
    path("connect-to-team/<int:event_id>/", views.assign_team, name='assign-team'),
    path("", views.list_team_events, name='list-team-events'),
    path("get-event-data/", views.get_events, name="get-events-data"),

]
