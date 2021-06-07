from django.db import models
from rest_framework import serializers
from .models import Text, Tag
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = ('__all__')

class TextSerializer(serializers.ModelSerializer):
    model = Text
    fields = ('__all__')