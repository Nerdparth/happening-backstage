from django.shortcuts import render
from users.models import BusinessAccount, TeamManager, TeamMember
# Create your views here.
def dashboard(request):
    account = BusinessAccount.objects.get(user=request.user)
    team = TeamManager.objects.get(user=account)
    return render(request, 'home/dashboard.html',context={'account':account,'team':team})