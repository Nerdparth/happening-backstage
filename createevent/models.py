from django.db import models

# Create your models here.
class EventDetails(models.Model):
    created_by = models.ForeignKey("users.BusinessAccount", on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=True)
    details = models.CharField(max_length=2000, null=True, blank=True)
    event_cateogry = models.CharField(max_length=50)
    event_date = models.DateField(default=None)
    event_time = models.TimeField(default=None)
    location = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='events',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    team = models.ForeignKey("users.TeamManager", on_delete=models.CASCADE, null=True)
    tickets = models.ForeignKey("EventTickets", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
class EventGuests(models.Model):
    name = models.CharField(max_length=30, null=False, blank=True)
    description = models.CharField(max_length=2000, null=False, blank=True)
    event = models.ForeignKey("EventDetails", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events',null=True, blank=True)
                              
    def __str__(self):
        return self.name
    
class EventTickets(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=2000, null=True, blank=True)
    event = models.ForeignKey("EventDetails", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_sold_out = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

