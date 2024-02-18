from .models import User
from rest_framework import serializers




class UserSerializer(serializers.ModelSerializer):
    """Показывает список пользователей(номеров телефона), которые ввели инвайт код текущего пользователя"""
    # invited_users = UserPublicSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'phone', 'referral_code', 'else_referral_code','activated']

