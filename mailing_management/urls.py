from django.urls import path
from mailing_management.apps import MailingManagementConfig

from mailing_management.views import IndexTemplateView, \
    MailingCreateView, del_mailing, \
    MailingUpdateView, LogListView

app_name = MailingManagementConfig.name

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('mailing_management/', MailingCreateView.as_view(),
         name='mailing_management'),
    path("del_mailing/<int:pk>/", del_mailing, name="del_mailing"),
    path("edit_mailing/<int:pk>/", MailingUpdateView.as_view(),
         name="edit_mailing"),

    path("logs/", LogListView.as_view(), name="logs"),
]
