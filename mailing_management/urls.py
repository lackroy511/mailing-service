from django.urls import path
from mailing_management.apps import MailingManagementConfig

from mailing_management.views import index, \
    MailingManagementCreateView, del_mailing, \
    MailingManagementUpdateView

app_name = MailingManagementConfig.name

urlpatterns = [
    path('', index, name='index'),

    # Управление пользователем

    # Управление рассылками
    path('mailing_management/', MailingManagementCreateView.as_view(),
         name='mailing_management'),
    path("del_mailing/<int:pk>/", del_mailing, name="del_mailing"),
    path("edit_mailing/<int:pk>/", MailingManagementUpdateView.as_view(),
         name="edit_mailing"),
]
