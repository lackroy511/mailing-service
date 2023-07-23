from django.urls import reverse_lazy
from django.views.generic import CreateView
from client_management.forms import ClientForm

from client_management.models import Client

# Create your views here.


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_management')
