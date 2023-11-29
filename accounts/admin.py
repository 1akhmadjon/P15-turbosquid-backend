from django.contrib import admin

from accounts.models import Role, UserRole

admin.site.register((Role, UserRole))