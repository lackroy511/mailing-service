from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, \
    TemplateView

from mailing_management.models import Mailing, MailingSettings, MailingLogs
from mailing_management.forms import MailingForm, MailingSettingsForm
from mailing_management.services import activate_mailing, \
    get_three_random_posts, is_manager_check, remove_mailing_cron_job, \
    get_page_obj_for_mailing, save_mailing_settings_periodicity, \
    start_mailing, upd_mailing_settings_periodicity, get_email_list_for_user, \
    deactivate_mailing, add_mailing_cron_job

from services.mixins import OwnerCheckMixin
from users.models import User


# Create your views here.

class IndexTemplateView(TemplateView):
    template_name = 'mailing_management/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = get_three_random_posts()

        context["posts"] = posts
        context["mailing_count"] = Mailing.objects.count()
        context["mailing_active_count"] = MailingSettings.objects.filter(
            mailing_status='отправляется').count()
        context["clients_count"] = User.objects.count()
        context['is_manager'] = is_manager_check(self)

        return context


class MailingCreateView(
        PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    permission_required = 'mailing_management.add_mailing'
    success_url = reverse_lazy('mailing_management:mailing_management')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings_form"] = MailingSettingsForm
        context['mailing_list'] = get_page_obj_for_mailing(self)
        context['is_manager'] = is_manager_check(self)

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

        add_mailing_cron_job(self=self, mailing=mailing,
                             mailing_settings=mailing_settings)

        email_list = get_email_list_for_user(mailing)

        start_mailing(self, mailing, mailing_settings, email_list)

        return super().form_valid(form)


class MailingUpdateView(
        PermissionRequiredMixin,
        LoginRequiredMixin, OwnerCheckMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    permission_required = 'mailing_management.change_mailing'
    success_url = reverse_lazy('mailing_management:mailing_management')

    def get_object(self, queryset=None):
        remove_mailing_cron_job(self=self)

        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings_form"] = MailingSettingsForm
        context['is_manager'] = is_manager_check(self)

        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        mailing = form.save()

        settings_form = MailingSettingsForm(self.request.POST)
        if settings_form.is_valid():
            mailing_settings = MailingSettings.objects.get(
                pk=mailing.mailingsettings.pk,
            )
            upd_mailing_settings_periodicity(mailing_settings, settings_form)

        add_mailing_cron_job(self=self, mailing=mailing,
                             mailing_settings=mailing_settings)

        return super().form_valid(form)


@permission_required('mailing_management.delete_mailing')
@login_required
def del_mailing(request, pk):
    try:

        mailing = Mailing.objects.get(pk=pk)
        if mailing.user != request.user:
            return redirect('mailing_management:index')

        remove_mailing_cron_job(pk=pk, request=request)
        mailing.delete()

    except ObjectDoesNotExist:
        return redirect('mailing_management:mailing_management')

    return redirect('mailing_management:mailing_management')


@permission_required('mailing_management.change_mailing')
def mailing_off(request, pk):

    if not request.user.groups.filter(name='manager').exists():
        return redirect('mailing_management:index')
    remove_mailing_cron_job(pk=pk, request=request)

    try:
        deactivate_mailing(pk)
    except ObjectDoesNotExist:
        return redirect('mailing_management:mailing_management')

    return redirect('mailing_management:mailing_management')


@permission_required('mailing_management.change_mailing')
def mailing_on(request, pk):

    if not request.user.groups.filter(name='manager').exists():
        return redirect('mailing_management:index')

    try:
        mailing = activate_mailing(pk)
    except ObjectDoesNotExist:
        return redirect('mailing_management:mailing_management')

    add_mailing_cron_job(mailing=mailing,
                         mailing_settings=mailing.mailingsettings)

    return redirect('mailing_management:mailing_management')


class LogListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = MailingLogs
    permission_required = 'mailing_management.view_mailinglogs'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = is_manager_check(self)

        return context
