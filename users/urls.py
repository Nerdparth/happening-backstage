from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("setup-business-account/",
        views.setup_business_account,
        name="setup-business-account",
    ),
    path("team-setup/", views.team_manager, name="team-setup"),
    path("add-members-page", views.add_to_team_page, name="add-members-page"),
    path("add-to-team", views.add_to_team, name="add-to-team"),
    
]
