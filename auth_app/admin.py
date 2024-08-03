from django.contrib import admin
from .models import Accounts

class AccAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active']
    list_editable = ['email', 'is_active']

admin.site.register(Accounts, AccAdmin)