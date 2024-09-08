from django.shortcuts import render, redirect
from .models import *
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import requests

# Create your views here.


def register_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = email.strip("@")[0]
        username+=get_random_string(4)
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        messages.success(request, 'Account created successfully')
        return HttpResponseRedirect('/users/setup-business-account')
    return render(request, 'users/register.html')


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = User.objects.get(email=email).username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('/home/dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return HttpResponseRedirect('/users/login')
    return render(request, 'users/login.html')

def setup_business_account(request):
    if request.method == "POST":
        user = request.user
        if not user:
            messages.error(request, 'User not logged in')
            return HttpResponseRedirect('/login')
        
        business_name = request.POST.get('business_name')
        business_address = request.POST.get('business_address')
        business_phone = request.POST.get('business_phone')
        business_email = request.POST.get('business_email')
        business_account = BusinessAccount(user=request.user, business_name=business_name, business_address=business_address, business_phone=business_phone, business_email=business_email)
        business_account.save()
        # make api call to email service to send email to user
        # if post_to_external_api(email=user.email,template="welcome",subject="Account setup successful",url="https://example.com",name=request.user.username,company_name=business_name,msg="Your account has been successfully setup") == 200:
        #     messages.success(request, 'Email Sent')   

        messages.success(request, 'Account setup successful')
        return HttpResponseRedirect('/users/team-setup')
    return render(request, 'users/account_setup_page.html')


def logout_user(request):
    logout(request)
    messages.error(request, 'Logout successful')
    return HttpResponseRedirect('/users/login')


@login_required
def dashboard(request):
    return render(request, 'home/dashboard.html')

def post_to_external_api(email,template,subject,url,name,company_name,msg):
    url = "https://email-service-d2hhazbgaeh8apga.eastus-01.azurewebsites.net/process-data/"
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
    return response.status_code
    
def team_manager(request):
    #creates a team in db
    if request.method == "POST":
        b_account = BusinessAccount.objects.get(user=request.user)

        team_name = request.POST.get('team_name')
        team_manager = TeamManager.objects.get_or_create(user=b_account, team_name=team_name)

        messages.success(request, 'Team created successfully')
        return HttpResponseRedirect('/users/add-members-page')
    return render(request, 'users/team_manager.html')


def add_to_team_page(request):
    try:
        b_account = BusinessAccount.objects.get(user=request.user)
        try:
            team = TeamManager.objects.get(user=b_account)
            return render(request, 'users/team-setup.html', {'team':team})
        except Exception as e:
            messages.error(request, 'No team found')
            return HttpResponseRedirect('/users/team-setup')
    except:
        messages.error(request, 'No business account found')
        return HttpResponseRedirect('users/setup-business-account/')




#jquery for this to add to team
@csrf_exempt
def add_to_team(request):
    if request.method == "POST":
        team_id = request.POST.get('team_id')
        team = TeamManager.objects.get(team_id=team_id)
        name = request.POST.get('name')
        role = request.POST.get('role')
        email = request.POST.get('email')
        team_member = TeamMember.objects.create(user=name,email=email, team=team, team_role=role)
        team_member.save()
        # if post_to_external_api(email=user.email,template="welcome",subject="Account setup successful",url="https://example.com",name=request.user.username,company_name=business_name,msg="Your account has been successfully setup") == 200:
        #     messages.success(request, 'Email Sent')  
        messages.success(request, 'Added to team successfully')
        return JsonResponse({'status':200, 'message':'Added to team successfully'})
    return render(request, 'users/add_to_team_page.html')