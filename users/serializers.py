from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'phone', 'referral_code', 'else_referral_code','activated']

