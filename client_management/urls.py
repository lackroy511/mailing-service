from django.urls import path

from client_management.apps import ClientManagementConfig
from client_management.views import ClientCreateView, ClientUpdateView, \
    delete_client

app_name = ClientManagementConfig.name

urlpatterns = [
    path('create/', ClientCreateView.as_view(), name='client_management'),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('delete/<int:pk>/', delete_client, name='delete_client'),
]
