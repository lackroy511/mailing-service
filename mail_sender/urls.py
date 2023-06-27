from django.urls import path
from mail_sender.apps import MailSenderConfig
from mail_sender.views import index

app_name = MailSenderConfig.name

urlpatterns = [
    path('', index, name='index'),
]

