from os import name
from django.urls import path
from .import views

urlpatterns = [
    path('', views.Account.as_view(), name='user'),
    path('login/', views.Login.as_view(), name='login'),
    path('snippets/', views.Snippet.as_view(), name='user-serializer'),
    path('count/', views.CountSnippets.as_view(), name='count'),
    path('snippet-specific/<str:title>/', views.SnippetSpecific.as_view(), name='snippet-specific'),
    path('tags/', views.ListTags.as_view(), name='tags'),
    path('specific-tag/<str:tag>/', views.SpecificTag.as_view(), name='specific-tag')
]