from django.urls import path
from mail_sender.apps import MailSenderConfig

from mail_sender.views import index, user_management, del_user, edit_user, \
    MailingManagementCreateView, del_mailing, MailingManagementUpdateView

app_name = MailSenderConfig.name

urlpatterns = [
    path('', index, name='index'),

    # Управление пользователем
    path('user_management/', user_management, name='user_management'),
    path('del_user/<int:pk>/', del_user, name='del_user'),
    path('edit_user/<int:pk>/', edit_user, name='edit_user'),

    # Управление рассылками
    path('mailing_management/', MailingManagementCreateView.as_view(),
         name='mailing_management'),
    path("del_mailing/<int:pk>/", del_mailing, name="del_mailing"),
    path("edit_mailing/<int:pk>/", MailingManagementUpdateView.as_view(),
         name="edit_mailing"),
]
