from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('applications/', ApplicationsView.as_view(), name='applications'),
    
    
    # For Endpoints
    path('application_submission/', application_submission, name='application_submission'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)