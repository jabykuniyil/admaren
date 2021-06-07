from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TagSerializer, UserSerializer, TextSerializer
from .models import Text, Tag
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.

#creating an account for the user.
class Account(APIView):
    def post(self, request):
        request.data['password'] = make_password(request.data['password'])
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

""" get function is used to get the all text snippets and count of the text snippets.
post function is used to create a new text snippet."""
class Snippet(APIView):
    
    def get(self, request):
        snippets = Text.objects.all()
        serializer = TextSerializer(snippets, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        text = request.data['text']
        title = request.data['title']
        if Text.objects.filter(title=title).exists():
            return Response({
                "message" : "The title already exists"
            })
        if User.objects.filter(id=request.data['user']).exists():
            user = User.objects.get(id=request.data['user'])
        else:
            return Response({
                "message" : "The user doesn't exist"
            })
        if 'tag' in request.data.keys():
            tag = request.data['tag']
            if Tag.objects.filter(tag=tag).exists():
                return Response({
                    "message" : "The tag already exists"
                })
            curr_tag = Tag.objects.filter(tag=tag).first()
            Text.objects.create(text=text, title=title, tag=curr_tag, user=user)
            curr_text = Text.objects.filter(title=title).first()
            Tag.objects.create(tag=tag, text=curr_text)
            return Response(status=status.HTTP_201_CREATED)
        Text.objects.create(text=text, title=title, user=user)
        return Response(status=status.HTTP_201_CREATED)
    

#this class is for to get the count of the snippets thar are stored on the database.
class CountSnippets(APIView):
    def get(self, request):
        count = Text.objects.all().count()
        return Response({
            "count of snippets" : count
            })
       
        
"""" The class for to access the specific data snippet.
The get function is used to get the particular snippet.
The put function is used to update the particular snippet.
The delete function is used to delete the particular snippet."""
class SnippetSpecific(APIView):
    
    def get(self, request, title):
        snippet = Text.objects.get(title=title)
        serializer = TextSerializer(snippet, many=False)
        return Response(serializer.data)
    
    def put(self, request, title):
        snippet = Text.objects.get(title=title)
        serializer = TextSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, title):
        snippet = Text.objects.get(title=title)
        snippet.delete()
        return Response({
            "message" : "The snippet has deleted successfully"
        })
        

#this class is for to list the tags are stored on the database.
class ListTags(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    

#this class is for to get the particular tag.
class SpecificTag(APIView):
    def get(self, request, tag):
        tag = Tag.objects.get(tag=tag)
        serializer = TagSerializer(tag, many=False)
        return Response(serializer.data)