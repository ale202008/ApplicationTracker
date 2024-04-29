from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.conf import settings
from apptracker.models import *
from datetime import date
import os
import json

# Create your views here.

def save_image(image):
    if image:
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename =  fs.save(image.name, image)
        return fs.url(filename)
    return None

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
    applied_status = Status.objects.get_or_create(name='Applied')
    
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

def get_applied_applications():
    status, _ = Status.objects.get_or_create(name='Applied')
    return list(Application.objects.filter(status=status).order_by('-id'))

def get_rejected_applications():
    status, _ = Status.objects.get_or_create(name='Rejected')
    return list(Application.objects.filter(status=status).order_by('-id'))

def get_interview_applications():
    status, _ = Status.objects.get_or_create(name='Interview')
    return list(Application.objects.filter(status=status).order_by('-id'))

def update_status(request):
    data = json.loads(request.body)
    status, _ = Status.objects.get_or_create(name=data.get("columnId"))
    application = Application.objects.get(id=data.get("applicationId"))
    
    application.status = status
    application.save()

    return JsonResponse({ "success": True})

class HomeView(View):
    def get(self, request):
        employment_choices = Application.EMPLOYMENT_CHOICES
        source_choices = list(Source.objects.order_by('name').values_list('name', flat=True)) if Source.objects.exists() else None
        employer_choices = list(Employer.objects.order_by('name').values_list('name', flat=True)) if Employer.objects.exists() else None
        location_choices = list(Location.objects.order_by('name').values_list('name', flat=True)) if Location.objects.exists() else None
        application_urls = list(Application.objects.exclude(img_url__isnull=True).values_list('img_url', flat=True))
        
        context = {
            'employment_choices': employment_choices,
            'source_choices': source_choices,
            'employer_choices': employer_choices,
            'location_choices': location_choices,
            'urls': application_urls,
        }
        
        return render(request, 'home.html', context)

class ApplicationsView(View):
    def get(self, request):
        context = {
            'applied_applications': get_applied_applications(),
            'rejected_applications': get_rejected_applications(),
            'interview_applications': get_interview_applications(),
        }
        return render(request, 'applications.html', context) 
    
class ChartView(View):
    def get(self, request):
        data =  [
                    {'from': "Applied", "to": "Rejected", "value": len(get_rejected_applications())},
                    {'from': "Applied", "to": "Interview", "value": len(get_interview_applications())},
                    {'from': "Applied", "to": "No Response", "value": len(get_applied_applications())},
                ]
        
        context = {
            "data": data
        }
        return render(request, 'chart.html', context) 