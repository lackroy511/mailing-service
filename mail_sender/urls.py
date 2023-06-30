from django.urls import path
from mail_sender.apps import MailSenderConfig

from mail_sender.views import index, user_management, del_user, edit_user

app_name = MailSenderConfig.name

urlpatterns = [
    path('', index, name='index'),
    
    path('user_management/', user_management, name='user_management'),
    path('del_user/<int:pk>/', del_user, name='del_user'),
    path('edit_user/<int:pk>/', edit_user, name='edit_user')
    
]

