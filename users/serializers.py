from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['phone']


class UserAuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'code']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone', 'referral_code', 'else_referral_code', 'activated']

class UserRefCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['else_referral_code']


