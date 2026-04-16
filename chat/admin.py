from django.contrib import admin
from .models import Thread, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['ad', 'updated_at']
    inlines = [MessageInline]
