from .models import *
from datetime import date
from .utils import *

def get_application_count():
    return Application.objects.count()

def applied_today():
    return Application.objects.filter(application_date=date.today()).exists()

def get_rate(status_name):
    total_applications = get_application_count()
    rate = 0
    if status_name == "Applied":
        rate = (get_response_count()/total_applications) * 100
    else:
        rate = (len(get_all_status_applications(status_name))/total_applications) * 100
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