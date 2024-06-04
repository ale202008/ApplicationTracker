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
        location_choices = Location.objects.order_by("state") if Location.objects.exists() else None

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
            'applications': get_all_applications().order_by('-application_id'),
            'statuses': get_all_statuses,
            'num_no_response': get_no_response_count(None),
            'num_rejected': get_status_application_count("Rejected", 0).count(),
            'num_interview': get_status_application_count("Interview", 1).count(),
            'num_withdrawn': get_status_application_count("Withdrawn", 0).count(),
            'num_offered': get_status_application_count("Offered", 0).count(),
            'num_accepted': get_status_application_count("Accepted", 0).count(),
        }
        return render(request, 'applications.html', context)

class ChartView(View):
    def get(self, request):
        context = {
            "sankeychart_data": get_sankeychart_data(),
            "heatmap_data": get_heatmap_data(),
            "map_data": get_map_data(),
            "miscstats_data": get_miscstats(),
            "source_stats_data": get_source_stats(),
            "current_month_stats_data": get_current_month_stats(),
            "location_stats_data": get_locations_stats(),
        }
        return render(request, 'chart.html', context) 