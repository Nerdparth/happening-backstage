from django.urls import path
from . import views

urlpatterns = [
    path("view-event/<int:id>", views.ViewEvent, name='view-event'),
    path("create-event", views.CreateEvent, name='create-event')
]
