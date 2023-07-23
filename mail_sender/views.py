from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from mail_sender.models import Client, Mailing, MailingSettings
from mail_sender.forms import MailingForm, MailingSettingsForm

# Create your views here.


def index(request):
    """
    Главная страница
    """

    context = {
        'is_active_main': 'active',
    }
    return render(request, 'mail_sender/index.html', context=context)


def user_management(request):
    """
    Управление пользователями
    """
    users_list = Client.objects.all()

    paginator = Paginator(users_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users_list': page_obj,
    }

    if request.method == 'POST':
        Client.objects.create(
            email=request.POST.get('email'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            surname=request.POST.get('surname'),
            comment=request.POST.get('comment'),
        )

    return render(request,
                  'mail_sender/mailing_management/user_management.html',
                  context=context)


def del_user(request, pk):
    """
    Управление пользователями: Удалить пользователя
    """
    try:
        Client.objects.get(pk=pk).delete()
    except ObjectDoesNotExist:
        return redirect('http://127.0.0.1:8000/user_management/')
    return redirect('http://127.0.0.1:8000/user_management/')


def edit_user(request, pk):
    """
    Управление пользователями: Редактировать пользователя.
    """
    user = Client.objects.get(pk=pk)

    context = {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'surname': user.surname,
        'comment': user.comment,
    }

    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.surname = request.POST.get('surname')
        user.comment = request.POST.get('comment')

        user.save()

        return redirect('http://127.0.0.1:8000/user_management/')

    return render(request,
                  'mail_sender/mailing_management/edit_user.html',
                  context=context)


class MailingManagementCreateView(CreateView):
    '''
    Управление рассылкой: Создание рассылки.
    '''
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mail_sender:mailing_management')
    template_name = 'mail_sender/mailing_management/mailing_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings_form"] = MailingSettingsForm

        mailing_list = Mailing.objects.all()
        paginator = Paginator(mailing_list, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['mailing_list'] = page_obj

        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        mailing = form.save()

        settings_form = MailingSettingsForm(self.request.POST)
        if settings_form.is_valid():
            mailing_settings = settings_form.save(commit=False)
            mailing_settings.mailing = mailing

            time = mailing_settings.mailing_time
            periodicity = mailing_settings.mailing_periodicity

            formatted_time = time.strftime('%M:%H')
            formatted_time = formatted_time.split(':')

            periodicity = periodicity.replace('M', formatted_time[1])
            periodicity = periodicity.replace('H', formatted_time[0])

            mailing_settings.mailing_periodicity = periodicity
            mailing_settings.save()

        return super().form_valid(form)


class MailingManagementUpdateView(UpdateView):
    '''
    Управление рассылкой: Создание рассылки.
    '''
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mail_sender:mailing_management')
    template_name = 'mail_sender/mailing_management/mailing_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings_form"] = MailingSettingsForm

        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        mailing = form.save()

        settings_form = MailingSettingsForm(self.request.POST)
        if settings_form.is_valid():

            mailing_settings = MailingSettings.objects.get(
                pk=mailing.mailingsettings.pk,
            )

            mailing_settings.mailing_time = \
                settings_form.cleaned_data['mailing_time']

            mailing_settings.mailing_periodicity = \
                settings_form.cleaned_data['mailing_periodicity']

            time = mailing_settings.mailing_time
            periodicity = mailing_settings.mailing_periodicity

            formatted_time = time.strftime('%M:%H')
            formatted_time = formatted_time.split(':')

            periodicity = periodicity.replace('M', formatted_time[1])
            periodicity = periodicity.replace('H', formatted_time[0])

            mailing_settings.mailing_periodicity = periodicity

            mailing_settings.save()

        return super().form_valid(form)


def del_mailing(request, pk):
    '''
    Управление рассылкой: Удаление рассылки.
    '''
    try:
        massage = Mailing.objects.get(pk=pk)
        massage.delete()
    except ObjectDoesNotExist:
        return redirect('mail_sender:mailing_management')
    return redirect('mail_sender:mailing_management')
