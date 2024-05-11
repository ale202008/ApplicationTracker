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
        
        context = {
            "data": data
        }
        return render(request, 'chart.html', context) 