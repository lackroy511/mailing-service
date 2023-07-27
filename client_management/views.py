from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, UpdateView

from client_management.forms import ClientForm
from client_management.models import Client
from client_management.services import get_page_obj_for_client

from services.mixins import OwnerCheckMixin

# Create your views here.


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_management')

    def form_valid(self, form):
        client = form.save(commit=False)
        client.user = self.request.user
        client.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["object_list"] = get_page_obj_for_client(self)
        return context


class ClientUpdateView(OwnerCheckMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_management')


def delete_client(request, pk):
    '''
    Управление рассылкой: Удаление клиента.
    '''
    try:
        client = Client.objects.get(pk=pk)

        if client.user != request.user:
            return redirect('mailing_management:index')

        client.delete()
    except ObjectDoesNotExist:
        return redirect('client:client_management')

    return redirect('client:client_management')
