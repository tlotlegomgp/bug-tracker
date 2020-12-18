from django.contrib import admin
from .models import Ticket, TicketComment, TicketAttachment, Project, ProjectRole, Todo

# Register your models here.

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'created_by', 'assigned_to', 'priority', 'class_type', 'status')
    search_fields = ('title', 'created_by', 'assigned_to', 'priority', 'class_type', 'status')

class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticket', 'body_message')
    search_fields = ('user', 'ticket')


class TicketAttachmentrAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'note', 'submitted_by', 'created_on', 'attachment')
    search_fields = ('ticket', 'submitted_by')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_on', 'created_by')
    search_fields = ('name', 'created_by')

class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'created_on')
    search_fields = ('user', 'project')

class TodoAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'created_on', 'note')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketComment, TicketCommentAdmin)
admin.site.register(TicketAttachment, TicketAttachmentrAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectRole, ProjectRoleAdmin)
admin.site.register(Todo, TodoAdmin)
