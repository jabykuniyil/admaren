from rest_framework import serializers
from .models import Text, Tag
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class TextSerializer(serializers.ModelSerializer):
    User = UserSerializer(read_only=True)
    class Meta:
        model = Text
        fields = ('__all__')


class TagSerializer(serializers.ModelSerializer):
    Text = TextSerializer(read_only=True)
    class Meta:
        model = Tag
        fields = ('__all__')