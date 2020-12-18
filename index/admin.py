from django.contrib import admin
from .models import Todo, DirectMessage

# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'created_on', 'note')


class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'receiver', 'body', 'created_on')
    search_fields = ('author', 'receiver')


admin.site.register(Todo, TodoAdmin)
admin.site.register(DirectMessage, DirectMessageAdmin)
