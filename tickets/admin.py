from django.contrib import admin
from .models import TicketComment, Ticket, TicketAttachment

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


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketComment, TicketCommentAdmin)
admin.site.register(TicketAttachment, TicketAttachmentrAdmin)
