from apptracker.models import *
import json
from django.http import JsonResponse


# Functions dedicated to grab applications based on requirements, in decreasing order

# ---- GET ALL FUNCTIONS --- #

# Function to get ALL applied applications
def get_all_status_applications(status_name):
    if Status.objects.filter(name=status_name).exists():
        status_list = Status.objects.filter(name=status_name)
    else:
        return None
    
    applications_list = Application.objects.filter(status__in=status_list).order_by('-id')
    return applications_list

# ---- GET ALL FUNCTIONS END --- #
# ---- GET FUNCTIONS --- #

# Function to get interview applications based on index in status list
def get_status_application_count(status_name, index):
    if status_name == "Rejected" and index == 1:
        return len(Application.objects.filter(status=Status.objects.filter(name="Rejected")[index-1]))
    status = Status.objects.filter(name=status_name)
    status_list = Status.objects.filter(status_id__gt = status[index-1].status_id - 1)
    applications_list = Application.objects.filter(status__in=status_list)
    return len(applications_list)

# Function to get all applications that have received a response
def get_response_count():
    return len(get_all_status_applications("Rejected")) + len(get_all_status_applications("Interview")) + len(get_all_status_applications("Withdrawn"))

# ---- GET FUNCTIONS END --- #

# Function that updates a status based on a drag-drop ui
def update_status(request):
    data = json.loads(request.body)
    application = Application.objects.get(id=data.get("applicationId"))
    status = data.get("columnId")
    status_list = Status.objects.filter(status_id__gt=application.status.status_id)
    
    if application.status.name == "Interview" and (status != "Applied" or status != "Offer"):
        temp_status = status_list.filter(name=status).first()
        if not temp_status:
            status = Status.objects.create(status_id=Status.objects.count() + 1, name=status)
            status.save()
        else:
            status = temp_status

    
    application.status = status
    application.save()

    return JsonResponse({ "success": True})