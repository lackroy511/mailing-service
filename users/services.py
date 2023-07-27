import jwt
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import redirect


from users.models import User


def get_token(user: User) -> str:
    """Сформировать токен для пользователя.
    Args:
        user (User): Класс модели пользователя

    Returns:
        str: Токен для пользователя
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    user_id = {'user_id': uid}
    token = jwt.encode(user_id, settings.SECRET_KEY, algorithm='HS256')

    return token


def form_massage(self, token: str) -> str:
    """Сформировать сообщение для активации пользователя.
    Args:
        token (str): Токен для активации пользователя.

    Returns:
       str: Сообщение для активации пользователя.
    """
    current_site = get_current_site(self.request)
    activation_link = reverse_lazy(
        'users:activate_user', kwargs={'token': token})
    activation_url = f"{current_site}{activation_link}"

    message = \
        f'Для активации аккаунта перейдите по ссылке:\n{activation_url}'

    return message


def get_id_from_token(token: str) -> dict:
    """Получить идентификатор пользователя из токена.
    Args:
        token (str): Токен для активации пользователя.

    Returns:
        dict: Словарь с идентификатором пользователя. Ключ - 'user_id'.
    """
    try:
        uid = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return redirect('users:activation_failed')

    return uid


def user_activation(uid: str) -> None:
    """Активировать пользователя.
    Args:
        uid (str): Идентификатор пользователя.
    """
    uidb64 = force_str(urlsafe_base64_decode(uid['user_id']))
    user = User.objects.get(pk=uidb64)
    user.is_active = True
    user.save()
