from django.contrib import admin

from main.models import Sections, Shoppingcart, Products, Image

# Register your models here.
admin.site.register((Sections, Shoppingcart, Products, Image))
