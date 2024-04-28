from django.db import models
from django.utils import timezone
from .models import *

# Create your models here.
class Source(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        managed=True

class Location(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        managed=True

class Employer(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        managed=True

class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Application(models.Model):
    # Everything a job application might have that I would like to record, and status of application
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    application_id = models.IntegerField(null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    position = models.CharField(max_length=255, null=False)
    pay = models.IntegerField(null=False)
    desc = models.TextField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)
    application_date = models.DateField(null=True, blank=True)
    img_url = models.URLField(null=True)
    
    REMOTE = "R"
    HYBRID = "H"
    INOFFICE = "IO"
    CONTRACT = "C"
    EMPLOYMENT_CHOICES = [
        (REMOTE, "Remote"),
        (HYBRID, "Hybrid"),
        (INOFFICE, "InOffice"),
        (CONTRACT, "Contract")
    ]    
    employment_type = models.CharField(max_length=10, choices=EMPLOYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def available_transitions(self):
        # Return a queryset of available transitions based on current status
        return Status.objects.filter(transitions_from=self.status)
    
    def __str__(self):
        return f"{self.application_id, self.position, self.location.name, self.employer.name}"
    
    class Meta:
        managed=True
