from django.urls import path
from .import views

urlpatterns = [
    path('', views.UserSerializer.as_view(), name='user-serializer')
]