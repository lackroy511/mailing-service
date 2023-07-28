from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from client_management.models import Client


from mailing_management.models import Mailing, MailingSettings
from mailing_management.forms import MailingForm, MailingSettingsForm
from mailing_management.services import add_mailing_cron_job, \
    remove_mailing_cron_job, \
    get_page_obj_for_mailing, save_mailing_settings_periodicity, \
    start_mailing, upd_mailing_settings_periodicity

from services.mixins import OwnerCheckMixin


# Create your views here.


def index(request):
    """
    Главная страница
    """
    context = {
        'is_active_main': 'active',
    }
    return render(request, 'mailing_management/index.html', context=context)


class MailingCreateView(CreateView):
    '''
    Управление рассылкой: Создание рассылки.
    '''
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing_management:mailing_management')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings_form"] = MailingSettingsForm

        context['mailing_list'] = get_page_obj_for_mailing(self)

        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        mailing = form.save(commit=False)
        mailing.user = self.request.user
        mailing.save()

        settings_form = MailingSettingsForm(self.request.POST)
        if settings_form.is_valid():
            mailing_settings = settings_form.save(commit=False)
            mailing_settings.mailing = mailing

            save_mailing_settings_periodicity(mailing_settings)

        add_mailing_cron_job(self, mailing, mailing_settings)

        email_list = [client.email for client in Client.objects.filter(
            user=self.request.user)]

        start_mailing(self, mailing, mailing_settings, email_list)

        return super().form_valid(form)


class MailingUpdateView(OwnerCheckMixin, UpdateView):
    '''
    Управление рассылкой: Создание рассылки.
    '''
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing_management:mailing_management')

    def get_object(self, queryset=None):
        remove_mailing_cron_job(self=self)

        return super().get_object(queryset)

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
            upd_mailing_settings_periodicity(mailing_settings, settings_form)

        add_mailing_cron_job(self, mailing, mailing_settings)

        return super().form_valid(form)


def del_mailing(request, pk):
    '''
    Управление рассылкой: Удаление рассылки.
    '''
    remove_mailing_cron_job(pk=pk, request=request)

    try:
        mailing = Mailing.objects.get(pk=pk)

        if mailing.user != request.user:
            return redirect('mailing_management:index')

        mailing.delete()
    except ObjectDoesNotExist:
        return redirect('mailing_management:mailing_management')

    return redirect('mailing_management:mailing_management')
