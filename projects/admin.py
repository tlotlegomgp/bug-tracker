from django.contrib import admin
from .models import Project, ProjectRole

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_on', 'created_by')
    search_fields = ('name', 'created_by')

class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'created_on')
    search_fields = ('user', 'project')


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectRole, ProjectRoleAdmin)
