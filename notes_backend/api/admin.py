from django.contrib import admin
from .models import Note

# PUBLIC_INTERFACE
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'created_at', 'updated_at']
    search_fields = ['title', 'user__username']
    list_filter = ['user', 'created_at', 'updated_at']
