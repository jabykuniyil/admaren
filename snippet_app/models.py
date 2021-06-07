from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Text(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, primary_key=True)
    text = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    
class Tag(models.Model):
    text = models.ForeignKey(Text, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.CharField(max_length=100, null=True, unique=True)