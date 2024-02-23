from django.urls import path

from users.apps import UsersConfig
from .views import UserRegistrationView, UserAuthorizationAPIView, UserProfileAPIView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

app_name = UsersConfig.name

urlpatterns = [
    # Регистация пользователя
    path('registration/', UserRegistrationView.as_view(), name='phone_authorization'),
    # Авторизация пользователя
    path('authorization/', UserAuthorizationAPIView.as_view(), name='code_authorization'),
    # Профиль пользователя
    path('user/<int:pk>/', UserProfileAPIView.as_view(), name='user-profile'),

    path('token/', TokenObtainPairView.as_view(), name="take_token"),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresh_token"),

]