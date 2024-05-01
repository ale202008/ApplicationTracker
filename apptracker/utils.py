from apptracker.models import *
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import date
import json

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
    if status_name == "Rejected":
        return len(Application.objects.filter(status=Status.objects.filter(name="Rejected")[index-1]))
    status = Status.objects.filter(name=status_name)
    status_list = Status.objects.filter(status_id__gt = status[index-1].status_id - 1)
    applications_list = Application.objects.filter(status__in=status_list)
    return len(applications_list)

# Function to get all applications that have received a response
def get_response_count():
    return len(get_all_status_applications("Rejected")) + len(get_all_status_applications("Interview")) + len(get_all_status_applications("Withdrawn"))

# ---- GET FUNCTIONS END --- #

# Function that saves an image
def save_image(image):
    if image:
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename =  fs.save(image.name, image)
        return fs.url(filename)
    return None

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
    image = save_image(request.FILES.get('image'))
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
        img_url=image,
        application_date = application_date,
    )
    application.save()
    
    return JsonResponse({'success': True})

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