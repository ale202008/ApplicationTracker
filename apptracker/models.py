from django.db import models
from django.utils import timezone

# Create your models here.
class Status(models.Model):
    # Holds all the potential statuses of application I might need while also allowing the ability to update and add
    name = models.CharField(max_length=50)
    # Creates a me to check which status leads into which
    transitions_from = models.ManyToManyField('self', symmetrical=False, related_name='transitions', blank=True)
    
    # Name
    def __str__(self):
        return self.name
    
    class Meta:
        managed=True

class Application(models.Model):
    # Everything a job application might have that I would like to record, and status of application
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    application_id = models.IntegerField(null=False)
    location = models.CharField(max_length=255, null=False)
    employer = models.CharField(max_length=255, null=False)
    position = models.CharField(max_length=255, null=False)
    pay = models.IntegerField(null=False)
    desc = models.TextField()
    source = models.CharField(max_length=100, null=True, blank=True)
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
    exployment_type = models.CharField(max_length=10, choices=EMPLOYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def available_transitions(self):
        # Return a queryset of available transitions based on current status
        return Status.objects.filter(transitions_from=self.status)
    
    class Meta:
        managed=True
