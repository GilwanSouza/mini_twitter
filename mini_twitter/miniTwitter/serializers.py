# miniTwitter/serializers.py
from rest_framework import serializers
from .models import Tweet, CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']

class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'conteudo', 'criado_em', 'curtidas']
