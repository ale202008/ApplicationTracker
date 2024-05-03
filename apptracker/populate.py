import os
import sys
import django
import json
from datetime import datetime

# Add your Django project directory to the Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# Manually configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracker.settings')
django.setup()

# Now you can import your Django models
from apptracker.models import *

def populateApplications():
    json_file = os.path.join(PROJECT_ROOT, 'apptracker', 'data', 'pastapplicationdata.json')

    with open(json_file, 'r') as f:
        data = json.load(f)

    applied_status = Status.objects.get(name='Applied')
    location = Location.objects.get(name="Remote")
    source= Source.objects.get(name="LinkedIn")

    for entry in data:
        employer_name = entry.get('Company')
        employer, _ = Employer.objects.get_or_create(name=employer_name)
        date = entry.get('Date')
        application_date = (datetime.strptime(date, "%m/%d/%Y")).strftime("%Y-%m-%d")

        Application.objects.create(
            status=applied_status,
            application_id = Application.objects.count() + 1,
            position=entry.get('Role'),
            pay=0,
            employer=employer,
            location=location,
            employment_type="R",
            source=source,
            desc=entry.get('Description'),
            notes=None,
            img_url=None,
            application_date=application_date,
        )

def update_models():
    status = Status.objects.get(status_id=3)
    # new_status = Status.objects.get(status_id=2)
    applications_list = Application.objects.filter(status=status)
    for application in applications_list:
        application.interview_counter += 1
        # application.status = new_status
        application.save()


# Call the function to populate applications
# populateApplications()
update_models()