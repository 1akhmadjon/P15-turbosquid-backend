from django.contrib import admin

from main.models import SectionsByType, Sections

# Register your models here.
admin.site.register((SectionsByType, Sections))
