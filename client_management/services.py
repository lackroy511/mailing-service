from django.core.paginator import Paginator

from client_management.models import Client


def get_page_obj_for_client(self) -> Paginator:
    """Создает объект пагинации для клиентов.
    Returns:
        Paginator: _description_
    """
    clients = Client.objects.filter(user=self.request.user)

    paginator = Paginator(clients, 5)
    page_number = self.request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
