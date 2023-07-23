from django.contrib import admin

from mailing_management.models import MailingSettings, MailingLogs, \
    Mailing
# Register your models here.


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """
    Настройки админки для сообщения для отправки.
    """
    list_display = ('massage_subject', 'massage_text')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    """
    Настройки админки для настроек рассылки.
    """
    list_display = ('mailing', 'mailing_periodicity', 'mailing_status')


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    """
    Настройки админки для логов рассылки.
    """
    list_display = ('last_try_date', 'try_status', 'mailing')
