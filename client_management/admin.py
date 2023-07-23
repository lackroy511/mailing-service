from django.contrib import admin

from client_management.models import Client

# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Настройки админки для клиента.
    """
    list_display = ('email', 'first_name', 'last_name', 'surname', 'comment')