from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from apptracker.models import *

# Create your views here.

class HomeView(View):
    def get(self, request):
        context = {}
        return render(request, 'home.html', context)
    
    def post(self, request):
        context = {}
        return render(request, 'home.html', context)