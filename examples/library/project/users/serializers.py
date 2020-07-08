from rest_framework import serializers

from .models import User


class UserBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'is_active')


class UserFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
