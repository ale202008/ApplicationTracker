from django.shortcuts import render
from django.views import View
from apptracker.models import *
from .utils import *
import os


class HomeView(View):
    def get(self, request):
        employment_choices = Application.EMPLOYMENT_CHOICES
        source_choices = list(Source.objects.order_by('name').values_list('name', flat=True)) if Source.objects.exists() else None
        employer_choices = list(Employer.objects.order_by('name').values_list('name', flat=True)) if Employer.objects.exists() else None
        location_choices = list(Location.objects.order_by('name').values_list('name', flat=True)) if Location.objects.exists() else None
        
        context = {
            'employment_choices': employment_choices,
            'source_choices': source_choices,
            'employer_choices': employer_choices,
            'location_choices': location_choices,
        }
        
        return render(request, 'home.html', context)

class ApplicationsView(View):
    def get(self, request):
        context = {
            'applied_applications': get_all_status_applications("Applied"),
            'rejected_applications': get_all_status_applications("Rejected"),
            'interview_applications': get_all_status_applications("Interview"),
            'withdrawn_applications': get_all_status_applications("Withdrawn"),
            'offered_applications': get_all_status_applications("Offered"),
            'accepted_applications': get_all_status_applications("Accepted"),
        }
        return render(request, 'applications.html', context) 
    
class ChartView(View):
    def get(self, request):
        data =  [
                    {'from': "Applied", "to": "No Response", "value": len(get_all_status_applications("Applied"))},
                    {'from': "Applied", "to": "Response", "value": get_response_count()},
                    {'from': "Response", "to": "Rejected", "value": get_status_application_count("Rejected", 1)},
                    {'from': "Response", "to": "1st Interview", "value": get_status_application_count("Interview", 1)},
                    {'from': "1st Interview", "to": "Rejected After 1st", "value": get_status_application_count("Rejected", 2)},
                    {'from': "1st Interview", "to": "Withdrawn After 1st", "value": get_status_application_count("Withdrawn", 1)},
                ]
        
        context = {
            "data": data
        }
        return render(request, 'chart.html', context) 