from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from apptracker.models import *

# Create your views here.

def application_submission(request):
    location = request.POST.get('location')
    print("LOCATION", location)
    
    
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
    