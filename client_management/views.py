from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, UpdateView

from client_management.forms import ClientForm
from client_management.models import Client

# Create your views here.


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_management')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        clients = Client.objects.all()

        paginator = Paginator(clients, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["object_list"] = page_obj
        return context


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_management')


def delete_client(request, pk):
    '''
    Управление рассылкой: Удаление клиента.
    '''
    try:
        massage = Client.objects.get(pk=pk)
        massage.delete()
    except ObjectDoesNotExist:
        return redirect('client:client_management')
    return redirect('client:client_management')
