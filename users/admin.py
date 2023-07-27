from django.contrib import admin

from users.models import User

# Register your models here.


# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active',)
    search_fields = ('email', 'first_name', 'last_name')
