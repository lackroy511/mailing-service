from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView, UserLoginView, ActivationSuccess, \
    ActivationFailed, activate_user, UserUpdateView, UserListView, \
    user_on, user_off
from django.contrib.auth.views import LogoutView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("profile/", UserUpdateView.as_view(), name="profile"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users_list/", UserListView.as_view(), name="users_list"),
    path("user_on/<int:pk>/", user_on, name="user_on"),
    path("user_off/<int:pk>/", user_off, name="user_off"),

    path('activate_user/<str:token>', activate_user,
         name='activate_user'),
    path('success/', ActivationSuccess.as_view(), name='activation_success'),
    path('failed/', ActivationFailed.as_view(), name='activation_failed'),
]
