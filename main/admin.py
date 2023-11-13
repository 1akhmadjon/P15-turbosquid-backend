from django.contrib import admin

from main.models import SectionsByType, Sections, Shoppingcart, Products, Image

# Register your models here.
admin.site.register((SectionsByType, Sections, Shoppingcart, Products, Image))
