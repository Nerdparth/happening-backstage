from django.db import models

# Create your models here.


class Meetings(models.Model):
    meet_id = models.CharField(max_length=100)
    started_at = models.DateTimeField(auto_now_add=True)
    meet_title = models.CharField(max_length=100)
    team = models.ForeignKey("users.TeamManager", on_delete=models.CASCADE)
    

    def __str__(self):
        return self.meet_id
    
class Whiteboard(models.Model):
    created_by = models.ForeignKey("users.BusinessAccount", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    board_id = models.CharField(max_length=100)
    
    def __str__(self):
        return self.meet.board_id