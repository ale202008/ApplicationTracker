from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Status)
admin.site.register(Source)
admin.site.register(Location)
admin.site.register(Employer)
admin.site.register(Application)