from django.contrib import admin

from mail_sender.models import Client, MailingSettings, MailingLogs, Mailing
# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Настройки админки для клиента.
    """
    list_display = ('email', 'first_name', 'last_name', 'surname', 'comment', )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """
    Настройки админки для сообщения для отправки.
    """
    list_display = ('massage_subject', 'massage_text', )


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    """
    Настройки админки для настроек рассылки.
    """
    list_display = ('mailing_periodicity', 'mailing_status', 'mailing')


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    """
    Настройки админки для логов рассылки.
    """
    list_display = ('last_try_date', 'try_status', 'mailing')
