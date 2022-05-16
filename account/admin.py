from django.contrib import admin
from account.models import AppUser, AdminUser

admin.site.register(AppUser)
admin.site.register(AdminUser)
