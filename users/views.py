from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwner
from users.utils import get_tokens_for_user, create_digit_code

from users.models import User
from users.serializers import UserSerializer, UserAuthorizationSerializer, UserProfileSerializer, UserRefCodeSerializer
from users.utils import create_invite_code
import time
from rest_framework import status, generics


class UserRegistrationView(generics.CreateAPIView):
    """
    Post запрос на регистрацию пользователя по номеру телефона. Проверяем на ввод телефона.
    Создаем пользователя и отправляем 4-значный код для авторизации.
    """

    serializer_class = UserSerializer

    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({'detail': 'Введите телефон'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(phone=phone)
        user.code = create_digit_code()
        user.save()
        time.sleep(2)
        print(f'Код авторизации: {user.code}')
        return Response({'phone': phone})


class UserAuthorizationAPIView(generics.CreateAPIView):
    """
    Post запрос для авторизации по 4-значному коду. Задаем поле code (код смотрим в консоли).
    Проверяем на ввод поля.
    Если код верный, то авторизируем пользователя, создаем и сохраняем инвайт код в БД, иначе выводим ошибку.
    """
    serializer_class = UserAuthorizationSerializer

    def post(self, request, *args, **kwargs):

        code = request.data.get('code')

        if not code:
            return Response({'detail': 'Введите код'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(code=code)
        except User.DoesNotExist:
            return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_400_BAD_REQUEST)

        if code == user.code:
            tokens = get_tokens_for_user(user)
            user.is_active = True
            user.referral_code = create_invite_code()
            user.code = None
            user.save()
            return Response({'detail': 'Авторизация успешно завершена!', "tokens": tokens}, status=status.HTTP_200_OK)

        else:
            return Response({'detail': 'Неверный код авторизации'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.RetrieveAPIView):
    """
    Get запрос на получение профиля пользователя, со списком пользователей,
    которые ввели инвайт код текущего пользователя.
    Patch запрос для ввода чужого инвайт кода в профиле, если он был введен ранее, то
    обрабатываем ошибку присваивания, если не был введен, то присваиваем введенный
    пользователем инвайт код и присваиваем полю activated значение True.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        method = self.request.method
        if method == 'PATCH':
            return UserRefCodeSerializer
        if method == 'GET':
            return UserProfileSerializer

    def get(self, request):
        user = self.request.user
        serializer = UserProfileSerializer(user)
        referral_code = user.referral_code
        users_list = User.objects.filter(else_referral_code=referral_code).values('phone')
        return Response([serializer.data, users_list], status=status.HTTP_200_OK)

    def patch(self, request):
        user = self.request.user
        else_referral_code = request.data.get('else_referral_code')
        user_ref_code = User.objects.filter(referral_code=else_referral_code)

        if not else_referral_code:
            return Response({'detail': 'Введите инвайт код'}, status=status.HTTP_400_BAD_REQUEST)

        if user.activated:
            return Response({'detail': 'Вы уже вводили инвайт код'}, status=status.HTTP_400_BAD_REQUEST)

        if user_ref_code:
            user.else_referral_code = else_referral_code
            user.activated = True
            user.save()
            return Response({'detail': 'Инвайт код успешно активирован'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Такого инвайт-кода не существует'}, status=status.HTTP_400_BAD_REQUEST)
