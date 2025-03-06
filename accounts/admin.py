from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account



class AccountAdmin(UserAdmin):
  model = Account
  list_display_links = ('email', 'first_name', 'last_name')
  list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
  search_fields = ('email', 'username')
  ordering = ('email',)

  fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superadmin', 'is_superuser')}),
    )

  readonly_fields = ('date_joined', 'last_login', 'password')

admin.site.register(Account, AccountAdmin)