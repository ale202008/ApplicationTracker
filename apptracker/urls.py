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
    path('temp_applications/', Temp_ApplicationsView.as_view(), name='temp_applications'),
    path('chart/', ChartView.as_view(), name='chart'),
    
    
    # For Endpoints
    path('application_submission/', application_submission, name='application_submission'),
    path('update_status/', update_status, name='update_status'),
    path('get_logo_links/', get_logo_links, name='get_links'),
    path('get_application_json/', get_application_json, name='get_application_json')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)