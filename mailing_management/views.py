from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from mailing_management.models import Mailing, MailingSettings
from mailing_management.forms import MailingForm, MailingSettingsForm
from mailing_management.services import SCRIPT_FILENAME, add_mailing_cron_job, \
    format_periodicity_to_cron_schedule, get_periodicity_display, remove_mailing_cron_job

from client_management.models import Client

from services.crontab_utils import add_cron_job, generate_cron_command, \
    remove_cron_job

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
            raw_periodicity = mailing_settings.mailing_periodicity

            mailing_settings.mailing_periodicity = \
                format_periodicity_to_cron_schedule(time, raw_periodicity)

            mailing_settings.mailing_periodicity_display = \
                get_periodicity_display(raw_periodicity)

            mailing_settings.save()

        add_mailing_cron_job(mailing, mailing_settings)

        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    '''
    Управление рассылкой: Создание рассылки.
    '''
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing_management:mailing_management')

    def get_object(self, queryset=None):
        remove_mailing_cron_job(self)

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

            time = settings_form.cleaned_data['mailing_time']
            raw_periodicity = settings_form.cleaned_data['mailing_periodicity']

            mailing_settings.mailing_time = time
            mailing_settings.mailing_periodicity = \
                format_periodicity_to_cron_schedule(time, raw_periodicity)
            mailing_settings.mailing_periodicity_display = \
                get_periodicity_display(raw_periodicity)

            mailing_settings.save()

        add_mailing_cron_job(mailing, mailing_settings)

        return super().form_valid(form)


def del_mailing(request, pk):
    '''
    Управление рассылкой: Удаление рассылки.
    '''
    remove_mailing_cron_job(pk=pk)
    try:
        massage = Mailing.objects.get(pk=pk)
        massage.delete()
    except ObjectDoesNotExist:
        return redirect('mailing_management:mailing_management')
    return redirect('mailing_management:mailing_management')
