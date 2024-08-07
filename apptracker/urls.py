from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .utils import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('applications/', ApplicationsView.as_view(), name='applications'),
    path('chart/', ChartView.as_view(), name='chart'),
    
    
    # For Endpoints
    path('application_submission/', application_submission, name='application_submission'),
    path('update_status/', update_status, name='update_status'),
    path('get_logo_links/', get_logo_links, name='get_links'),
    path('get_application_json/', get_application_json, name='get_application_json'),
    path('get_navbar_stats/', get_navbar_stats, name='get_navbar_stats'),
    path('get_glassdoor_review_score/', get_glassdoor_score, name='get_glassdoor_review_score')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)