from .models import *
from datetime import date
from .utils import *

def get_application_count():
    return Application.objects.count()

def applied_today():
    return Application.objects.filter(application_date=date.today()).exists()

def get_rate(status_name):
    total_response_applications = get_response_count()
    total_status_applications = get_status_application_count(status_name, 1)
    
    if total_status_applications == 0: return 0
    if status_name == "Applied":
        rate = (total_response_applications/total_status_applications) * 100
    else:
        rate = (total_status_applications/total_response_applications) * 100
        
    return round(rate, 2)

def common_data(request):
    return {
        'applicationcount': get_application_count(),
        'appliedtoday': applied_today(),
        'responserate': get_rate("Applied"),
        'rejectionrate': get_rate("Rejected"),
        'interviewrate': get_rate("Interview"),
        'withdrawnrate': get_rate("Withdrawn"),
        'offeredrate': get_rate("Offered"),
        'acceptedrate': get_rate("Accepted"),
    }