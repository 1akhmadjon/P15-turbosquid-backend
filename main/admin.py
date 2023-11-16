from django.contrib import admin

from .models import Sections, Shoppingcart, Products, Image

# Register your models here.
admin.site.register(( Sections, Shoppingcart, Products, Image))
