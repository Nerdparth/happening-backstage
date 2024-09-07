from django.contrib import admin
from .models import BusinessAccount, TeamManager, TeamMember

admin.site.register(BusinessAccount)
admin.site.register(TeamManager)
admin.site.register(TeamMember)
# Register your models here.
