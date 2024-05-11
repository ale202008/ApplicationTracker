from apptracker.models import *
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import date
import json

# Functions dedicated to grab applications based on requirements, in decreasing order

# ---- GET ALL FUNCTIONS ---- #

# Function to get ALL applied applications
def get_all_status_applications(status_name):
    status = Status.objects.get(name=status_name)
    
    if status:
        return Application.objects.filter(status=status).order_by('-id')
    else:
        return None

# ---- GET ALL FUNCTIONS END ---- #
# ---- GET FUNCTIONS ---- #

# Function to get interview applications based on index in status list
def get_status_application_count(status_name, index):
    status = Status.objects.get(name=status_name)
    if status_name != "Interview":
        return Application.objects.filter(interview_counter=index, status=status)
    else:
        return Application.objects.filter(interview_counter__gte=index)

# Function to get all applications that have received a response
def get_response_count():
    return (Application.objects.count() - len(get_all_status_applications("Applied"))) - len(get_status_application_count("Withdrawn", 0))

# Function that returns the count of Application objects
def get_application_count():
    return Application.objects.count()

# Function that correctly labels and sends the values for the Sankey chart display
def get_sankeychart_data():
    applied_label = "[bold]Applied[/] " + "(" + str(Application.objects.count()) + ")"
    no_response_label = "[bold]No Response[/] " + "(" + str(get_response_count()) + ")"
    response_label =  "[bold]Response[/] " + "(" + str(get_response_count()) + ")"
    rejected_label = "[bold]Rejected[/] " + "(" + str(len(get_status_application_count("Rejected", 0))) + ")"
    withdrawn_label = "[bold]Withdrawn[/] " + "(" + str(len(get_status_application_count("Withdrawn", 0))) + ")"
    first_interview_label = "[bold]1st Interview[/] " + "(" + str(len(get_status_application_count("Interview", 1))) + ")"
    second_interview_label = "[bold]2nd Interview[/] " + "(" + str(len(get_status_application_count("Interview", 2))) + ")"
    rejected_after_first_label =  "[bold]Rejected After 1st[/] " + "(" + str(len(get_status_application_count("Rejected", 1))) + ")"
    withdrawn_after_first_label = "[bold]Withdrawn After 1st[/] " + "(" + str(len(get_status_application_count("Withdrawn", 1))) + ")"
    
    data =  [
                {'from': applied_label, "to": no_response_label, "value": len(get_all_status_applications("Applied")), "labelText": "Node 1 (100)"},
                {'from': applied_label, "to": response_label, "value": get_response_count()},
                {'from': applied_label, "to": withdrawn_label, "value": len(get_status_application_count("Withdrawn", 0))},
                {'from': response_label, "to": rejected_label, "value": len(get_status_application_count("Rejected", 0))},
                {'from': response_label, "to": first_interview_label, "value": len(get_status_application_count("Interview", 1))},
                {'from': first_interview_label, "to": rejected_after_first_label, "value": len(get_status_application_count("Rejected", 1))},
                {'from': first_interview_label, "to": withdrawn_after_first_label, "value": len(get_status_application_count("Withdrawn", 1))},
                {'from': first_interview_label, "to": second_interview_label, "value": len(get_status_application_count("Interview", 2))},
            ]
    
    return data

# ---- GET FUNCTIONS END ---- #
# ---- BOOLEAN FUNCTION ---- #

# Function that returns a boolean based if an Application object exists with today's date
def applied_today():
    return Application.objects.filter(application_date=date.today()).exists()

# ---- BOOLEAN FUNCTION END ---- #
# ---- MISC FUNCTIONS ---- #

# Function that saves an image
def save_url(url, employer):
    if url and not employer.website_url:
        employer.website_url = url
        employer.save()

# Function that submits a new application submission
def application_submission(request):
    position = request.POST.get('position')
    pay = request.POST.get('pay')
    employer_name = request.POST.get('employer') or request.POST.get('other_employer')
    employer, _ = Employer.objects.get_or_create(name=employer_name) if employer_name else (None, None)
    location_name = request.POST.get('location') or request.POST.get('other_location')
    location, _ = Location.objects.get_or_create(name=location_name) if location_name else (None, None)
    employment_type = request.POST.get('employment_type')
    source_name = request.POST.get('source') or request.POST.get('other_source')
    source, _ = Source.objects.get_or_create(name=source_name) if source_name else (None, None)
    description = request.POST.get('description')
    notes = request.POST.get('notes')
    save_url(request.POST.get('websiteurl'), employer)
    application_date = request.POST.get('application_date')
    applied_status = Status.objects.get(status_id=1, name='Applied')
    
    application = Application.objects.create(
        status=applied_status,
        application_id = Application.objects.count() + 1,
        position=position,
        pay=pay,
        employer=employer,
        location=location,
        employment_type=employment_type,
        source=source,
        desc=description,
        notes=notes,
        application_date = application_date,
    )
    application.save()
    
    return JsonResponse({'success': True})

# Function that updates a status based on a drag-drop ui
def update_status(request):
    data = json.loads(request.body)
    application = Application.objects.get(id=data.get("applicationId"))
    if application.status.name != "Interview" and application.status.name != "Applied":
        return JsonResponse({ "error": "Application status cannot be changed to new status." }, status=500)
    status = Status.objects.get(name=data.get("columnId"))
    if status.name == "Interview":
        application.interview_counter += 1
        
    application.status = status
    application.save()

    return JsonResponse({ "success": True})

# Function that calculates the rate for the given status out of all Application objects
def calc_rate(status_name):
    total_applications = get_application_count()
    rate = 0
    if status_name == "Applied":
        rate = (get_response_count()/total_applications) * 100
    else:
        rate = (len(get_all_status_applications(status_name))/total_applications) * 100
    return round(rate, 2)

# ---- MISC FUNCTIONS END ---- #
