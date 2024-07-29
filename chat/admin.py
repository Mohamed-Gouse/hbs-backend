from django.contrib import admin
from .models import Message

# Register your models here.
class MessageAdminView(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'messages', 'time',)

admin.site.register(Message, MessageAdminView)