from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.


class BusinessAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    business_address = models.CharField(max_length=100)
    business_phone = models.CharField(max_length=100)
    business_email = models.EmailField()

    def __str__(self):
        return self.business_name


team_roles = (("admin", "admin"), ("member", "member"), ("guest", "guest"))


class TeamManager(models.Model):
    user = models.ForeignKey("BusinessAccount", on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    team_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    # team_members = models.ManyToManyField(User, related_name='team_members')

    def __str__(self):
        return self.team_name
    
    def members(self):
        return TeamMember.objects.filter(team=self)


class TeamMember(models.Model):
    email = models.EmailField(blank=False,default="abc@gmail.com")
    user = models.CharField(max_length=100)
    team = models.ForeignKey("TeamManager", on_delete=models.CASCADE)
    team_role = models.CharField(max_length=100, choices=team_roles)

    def __str__(self):
        return self.email
