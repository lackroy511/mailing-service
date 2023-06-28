from django.contrib import admin

from mail_sender.models import Client, MassageToSend, MailingSettings, MailingLogs
# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Настройки админки для клиента.
    """
    list_display = ('email', 'full_name', 'comment', )


@admin.register(MassageToSend)
class ClientAdmin(admin.ModelAdmin):
    """
    Настройки админки для сообщения для отправки.
    """
    list_display = ('massage_subject', 'massage_text', 'mailing_settings', )


@admin.register(MailingSettings)
class ClientAdmin(admin.ModelAdmin):
    """
    Настройки админки для настроек рассылки.
    """
    list_display = ('mailing_time', 'mailing_periodicity', 'mailing_status', )


@admin.register(MailingLogs)
class ClientAdmin(admin.ModelAdmin):
    """
    Настройки админки для логов рассылки.
    """
    list_display = ('last_try_date', 'try_status',
                    'server_response', 'client', 'massage_to_send', )
