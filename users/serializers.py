from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'phone', 'password', 'referral_code', 'else_referral_code', 'activated']


class UserAuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'code']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone', 'referral_code', 'else_referral_code', 'activated']

class UserEnterCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'else_referral_code', 'activated']
