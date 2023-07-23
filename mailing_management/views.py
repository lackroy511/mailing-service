from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from mailing_management.models import Mailing, MailingSettings
from mailing_management.forms import MailingForm, MailingSettingsForm

# Create your views here.


def index(request):
    """
    Главная страница
    """
    context = {
        'is_active_main': 'active',
    }
    return render(request, 'mailing_management/index.html', context=context)


class MailingManagementCreateView(CreateView):
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
    success_url = reverse_lazy('mailing_management:mailing_management')

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
        return redirect('mailing_management:mailing_management')
    return redirect('mailing_management:mailing_management')
