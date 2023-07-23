from django.urls import path
from mailing_management.apps import MailingManagementConfig

from mailing_management.views import index, \
    MailingCreateView, del_mailing, \
    MailingUpdateView

app_name = MailingManagementConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('mailing_management/', MailingCreateView.as_view(),
         name='mailing_management'),
    path("del_mailing/<int:pk>/", del_mailing, name="del_mailing"),
    path("edit_mailing/<int:pk>/", MailingUpdateView.as_view(),
         name="edit_mailing"),
]
