from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=250,unique=True)
    User_ID = models.AutoField(primary_key=True)
    address = models.CharField(max_length=250, blank=True,null=True)
    session_token = models.CharField(max_length=20, default=0)
    phone = models.CharField(blank=True,null=True,max_length=20)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # standard