from django.contrib import admin

from .models import Sections, Shoppingcart, Products, Image, Category, Order, UserBalance, ArchiveShoppingcart, \
    ProductType, Format

# Register your models here.
admin.site.register(
    (Category, Sections, Shoppingcart, Products, Image, Order, UserBalance, ArchiveShoppingcart, Format, ProductType))
