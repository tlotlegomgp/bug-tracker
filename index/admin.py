from django.contrib import admin
from .models import Todo, DirectMessage, Alert

# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'created_on', 'note')


class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'receiver', 'body', 'created_on')
    search_fields = ('author', 'receiver')


class AlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'created_on')


admin.site.register(Todo, TodoAdmin)
admin.site.register(DirectMessage, DirectMessageAdmin)
admin.site.register(Alert, AlertAdmin)
