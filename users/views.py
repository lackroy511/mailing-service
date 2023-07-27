# from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail

from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy
from django.shortcuts import redirect

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from users.models import User
from users.services import form_massage, get_id_from_token, get_token, \
    user_activation


# Create your views here.


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('mailing:index')
    extra_context = {
        'is_active_register': 'active',
    }

    def form_valid(self, form):
        user = form.save()

        token = get_token(user)
        subject = 'Активация аккаунта'
        message = form_massage(self, token)

        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return super().form_valid(form)


def activate_user(request, token):

    uid = get_id_from_token(token)

    try:
        user_activation(uid)
    except (TypeError, ValueError, KeyError, User.DoesNotExist):
        return redirect('users:activation_failed')

    return redirect('users:activation_success')


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'
    extra_context = {
        'is_active_login': 'active',
    }


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserUpdateForm
    extra_context = {
        'is_active_profile': 'active',
    }

    def get_object(self, queryset=None):
        return self.request.user


class ActivationSuccess(TemplateView):
    template_name = 'users/activation_success.html'


class ActivationFailed(TemplateView):
    template_name = 'users/activation_failed.html'
