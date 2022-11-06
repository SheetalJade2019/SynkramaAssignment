from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    User_ID = models.AutoField(primary_key=True)
    address = models.CharField(max_length=250, default='Yes')
    phone = models.CharField(blank=True,null=True,max_length=20)
    is_admin = models.BooleanField(default=False)
    # standard