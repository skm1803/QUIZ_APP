from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


from .models import User

class UserAdmin(admin.ModelAdmin):
	list_display = ['email','active','staff']
	list_filter  = ['active']
	search_fields= ['email']

admin.site.register(User,UserAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)