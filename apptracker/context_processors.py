from .models import *
from datetime import date

def get_application_count():
    return Application.objects.count()

def applied_today():
    return Application.objects.filter(application_date=date.today()).exists()

def common_data(request):
    return {
        'applicationcount': get_application_count(),
        'appliedtoday': applied_today(),
    }