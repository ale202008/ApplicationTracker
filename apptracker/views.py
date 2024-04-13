from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from apptracker.models import *

# Create your views here.

def application_submission(request):
    position = request.POST.get('position')
    pay = request.POST.get('pay')
    employer = request.POST.get('employer') if request.POST.get('employer') else request.POST.get('other_employer')
    location = request.POST.get('location') if request.POST.get('location') else request.POST.get('other_location')
    employment_type =  request.POST.get('employment_type')
    source = request.POST.get('source') if request.POST.get('source') else request.POST.get('other_source')
    description = request.POST.get('description')
    notes = request.POST.get('notes')
    
    print(
        "Position:", position,
        "Pay:", pay,
        "employer:", employer,
        "location:", location,
        "employment_type:", employment_type,
        "source:", source,
        "description:", description,
        "notes:", notes,
    )
    

    
    
    return JsonResponse({'success': True})
    

class HomeView(View):
    def get(self, request):
        employment_choices = Application.EMPLOYMENT_CHOICES
        source_choices = Source.objects.all() if Source.objects.exists() else None
        employer_choices = Employer.objects.all() if Employer.objects.exists() else None
        location_choices = Location.objects.all() if Location.objects.exists() else None
        
        context = {
            'employment_choices': employment_choices,
            'source_choices': source_choices,
            'employer_choices': employer_choices,
            'location_choices': location_choices,
        }
        
        return render(request, 'home.html', context)
    