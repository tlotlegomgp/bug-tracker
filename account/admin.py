from django.contrib import admin
from account.models import Account, Profile
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_created', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_created', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'website', 'address')
    search_fields = ('user__username', 'first_name', 'last_name')


admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)
