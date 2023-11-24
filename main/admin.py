from django.contrib import admin

from .models import Sections, Shoppingcart, Products, Image, Category

# Register your models here.
admin.site.register((Sections, Shoppingcart, Products, Image, Category))

from .models import Category, Sections, Shoppingcart, Products, Image, Order, UserBalance, ArchiveShoppingcart

# Register your models here.
admin.site.register((Category, Sections, Shoppingcart, Products, Image, Order, UserBalance, ArchiveShoppingcart))
