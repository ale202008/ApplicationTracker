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