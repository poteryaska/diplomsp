from django.urls import path

from users.apps import UsersConfig
from .views import UserRegistrationView, UserAuthorizationAPIView, UserProfileAPIView, UserListCodesAPIView, UserEnterCodeAPIView

app_name = UsersConfig.name

urlpatterns = [
    # Регистация пользователя
    path('registration/', UserRegistrationView.as_view(), name='phone_authorization'),
    # Авторизация пользователя
    path('authorization/', UserAuthorizationAPIView.as_view(), name='code_authorization'),
    # Профиль пользователя
    path('user/<str:username>/', UserProfileAPIView.as_view(), name='user-profile'),
    # Просмотр списка пользователей, которые ввели инвайт-код текущего пользователя
    path('list-codes/', UserListCodesAPIView.as_view(), name='list-codes'),
    # Ввод чужого инвайт-кода в профиле
    path('enter-code/', UserEnterCodeAPIView.as_view(), name='enter-rcode'),

]