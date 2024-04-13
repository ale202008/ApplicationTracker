from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    
    
    # For Endpoints
    path('application_submission/', application_submission, name='application_submission'),
    
]