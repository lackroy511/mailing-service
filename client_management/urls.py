from django.urls import path

from client_management.apps import ClientManagementConfig
from client_management.views import ClientCreateView

app_name = ClientManagementConfig.name

urlpatterns = [
    path('create/', ClientCreateView.as_view(), name='client_management'),
]
