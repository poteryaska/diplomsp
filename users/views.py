from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer, UserAuthorizationSerializer, UserEnterCodeSerializer, \
    UserProfileSerializer
from users.utils import create_invite_code
import time
from rest_framework import status, generics

from django.shortcuts import get_object_or_404


class UserRegistrationView(generics.CreateAPIView):
    """
    Post запрос на регистрацию пользователя по заданный полям. Проверяем на ввод заданных полей.
    Создаем пользователя с указанными данными, если у него нет значения поля referral_code, то присваиваем ему
    значение с помошью метода create_invite_code, описан в utils.py.
    Проверяем на пустоту поле else_referral_code, если оно заполнено, то полю activated присваиваем True,
    в дефолтном значении False, возвращаем данные в ответе.
    """

    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        phone = request.data.get('phone')
        password = request.data.get('password')
        else_referral_code = request.data.get('else_referral_code')

        if not password:
            return Response({'detail': 'Введите пароль'}, status=status.HTTP_400_BAD_REQUEST)

        if not phone:
            return Response({'detail': 'Введите телефон'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(username=username, phone=phone, password=password,
                                                   else_referral_code=else_referral_code)

        if created or not user.referral_code:
            user.referral_code = create_invite_code()
            user.save()
            time.sleep(2)
        if else_referral_code is not None:
            user.activated = True
            user.save()

        return Response(
            {'phone': phone, 'username': username, 'referral_code': user.referral_code, 'password': password,
             'else_referral_code': else_referral_code})


class UserAuthorizationAPIView(generics.CreateAPIView):
    """
    Post запрос для авторизации по 4-значному коду. Задаем поля username (для поиска нужного пользователя)
    и code (код смотрим в БД). Проверяем на ввод этих полей.
    Если код верный, то авторизируем пользователя, иначе выводим ошибку.
    """
    serializer_class = UserAuthorizationSerializer
    def post(self, request):
        username = request.data.get('username')
        code = request.data.get('code')

        if not code:
            return Response({'detail': 'Введите код'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_400_BAD_REQUEST)

        if code == user.code:
            user.is_active = True
            user.save()
            time.sleep(2)
            return Response({'detail': 'Авторизация успешно завершена!'}, status=status.HTTP_200_OK)

        else:
            return Response({'detail': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.RetrieveAPIView):
    """
    Get запрос на получение профиля пользователя, со списком пользователей,
    которые ввели инвайт код текущего пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        referral_code = user.referral_code
        users = User.objects.filter(else_referral_code=referral_code).values('username', 'phone')
        users_list = list(users)
        return Response([serializer.data, users_list], status=status.HTTP_200_OK)


class UserEnterCodeAPIView(generics.CreateAPIView):
    """
    Post запрос для ввода чужого инвайт кода, если он был введен при регистрации, то
    обрабатываем ошибку присваивания, если при регистрации он не был введен,
    то присваиваем введенный пользователем инвайт код и присваиваем полю activated значение True.
    """
    serializer_class = UserEnterCodeSerializer
    def post(self, request):
        else_referral_code = request.data.get('else_referral_code')
        username = request.data.get('username')

        if not else_referral_code:
            return Response({'detail': 'Введите инвайт код'}, status=status.HTTP_400_BAD_REQUEST)

        if not username:
            return Response({'detail': 'Введите имя'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)
        if user.activated:
            return Response({'detail': 'Вы уже вводили инвайт код'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.else_referral_code = else_referral_code
            user.activated = True
            user.save()
            return Response({'detail': 'Инвайт код успешно активирован'}, status=status.HTTP_400_BAD_REQUEST)

