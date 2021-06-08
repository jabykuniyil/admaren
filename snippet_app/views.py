from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TagSerializer, UserSerializer, TextSerializer
from .models import Text, Tag
from django.contrib.auth.hashers import make_password, check_password
from functools import wraps
import datetime, jwt, os
from binascii import hexlify


secret_key = hexlify(os.urandom(50))

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
    

#login function with generating tokens.
class Login(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("The User not found")
        if check_password(password, user.password): 
            payload = {
                'id' : user.id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                'iat' : datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, secret_key, algorithm='HS256')
            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                'jwt' : token
            }
            return response
        return Response({
            "message" : "Invalid Password"
        })
        
            
""" get function is used to get the all text snippets and count of the text snippets.
post function is used to create a new text snippet."""
class Snippet(APIView):
    
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('UnAuthenticated!')
        try:
            snippets = Text.objects.all()
            serializer = TextSerializer(snippets, many=True)
            return Response(serializer.data)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        
    
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('UnAuthenticated!')
        try:
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
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        
    
#this class is for to get the count of the snippets thar are stored on the database.
class CountSnippets(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('UnAuthenticated!')
        try:
            count = Text.objects.all().count()
            return Response({
                "count of snippets" : count
                })
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
       
        
"""" The class for to access the specific data snippet.
The get function is used to get the particular snippet.
The put function is used to update the particular snippet.
The delete function is used to delete the particular snippet."""
class SnippetSpecific(APIView):
    
    def get(self, request, title):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('UnAuthenticated!')
        try:
            snippet = Text.objects.filter(title=title).first()
            if snippet is not None:
                serializer = TextSerializer(snippet, many=False)
                return Response(serializer.data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
    
    def put(self, request, title):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('UnAuthenticated!')
        try:
            snippet = Text.objects.filter(title=title).first()
            if snippet is not None:
                serializer = TextSerializer(snippet, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
    
    def delete(self, request, title):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('UnAuthenticated!')
        try:
            snippet = Text.objects.get(title=title)
            snippet.delete()
            return Response({
                "message" : "The snippet has deleted successfully"
            })
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        

#this class is for to list the tags are stored on the database.
class ListTags(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('UnAuthenticated!')
        try:
            tags = Tag.objects.all()
            serializer = TagSerializer(tags, many=True)
            return Response(serializer.data)            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
    

#this class is for to get the particular tag.
class SpecificTag(APIView):
    def get(self, request, tag):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('UnAuthenticated!')
        try:
            tag = Tag.objects.get(tag=tag)
            serializer = TagSerializer(tag, many=False)
            return Response(serializer.data)            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')