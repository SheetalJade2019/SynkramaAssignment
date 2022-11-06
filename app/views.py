from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from app.serializers import *

# Create your views here.
"""
register user & create student
"""
@api_view(['POST'])
def register_user(request):
    try:
        print("data ",request.data)
        first_name = request.data.get('first_name',None)
        last_name = request.data.get('last_name',None)
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        username = request.data.get('username',None)
        address = request.data.get('address',None)
        phone = request.data.get('phone',None)
        is_admin = request.data.get('is_admin',False)

        if not username or not password or not email:
            return Response({"mesg":"Please Enter all details"},status=status.HTTP_400_BAD_REQUEST) 

        user = User.objects.create(username=username,email=email,first_name=first_name,last_name=last_name,phone=phone,address=address, is_admin=is_admin)
                # password = uuid.uuid4() #create seed password
        user.set_password(password)
        user.save()
        return Response({"msg":"User Registered"},status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"msg":"Something went wrong"},status=500)

# @csrf_exempt
@api_view(['POST'])
def login_request(request):
    try:
        password = request.data.get('password',None)
        username = request.data.get('username',None)
        if not password or not username:
            return Response({"mesg":"Please Enter credentials"},status=status.HTTP_400_BAD_REQUEST) 

        user = authenticate(username=username,password=password)
        
        # if user.is_authenticated():
            # return Response({"mesg":"Already logged in"}, status=status.HTTP_200_OK)
        if user:
            login(request,user)
            return Response({"mesg":"User logged in"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"Invalid credentials"},status=status.HTTP_200_OK)
        
    except Exception as e:
        print(e)
        print(
        type(e).__name__,          # TypeError
        __file__,                  # /tmp/example.py
        e.__traceback__.tb_lineno  # 2
        )  
        return Response({"msg":"Something went wrong"},status=500)

@csrf_exempt
@api_view(['PUT'])
def update_student(request):
    try:
        print("data ",request.data)
        User_ID = request.data.get("User_ID",None)
        first_name = request.data.get('first_name',None)
        last_name = request.data.get('last_name',None)
        # email = request.data.get('email',None)
        password = request.data.get('password',None)
        # username = request.data.get('username',None)
        address = request.data.get('address',None)
        phone = request.data.get('phone',None)
        # standard = request.data.get("standard",None)
        is_admin = request.data.get('is_admin',False)

        # if not username or not password or not email:
            # return Response({"mesg":"Please Enter all details"},status=status.HTTP_400_BAD_REQUEST) 

        user = User.objects.get(User_ID=User_ID)
        if first_name:
            user.first_name=first_name
        if last_name:
            user.last_name=last_name
        if password:
            user.set_password(password)
        if address:
            user.address=address
        if phone:
            user.phone=phone
        user.save()
        return Response({"msg":"Student Updated"},status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        print(
        type(e).__name__,          # TypeError
        __file__,                  # /tmp/example.py
        e.__traceback__.tb_lineno  # 2
        )  
        return Response({"msg":"Something went wrong"},status=500)

@api_view(['DELETE'])
def delete_student(request):
    try:
        print("data ",request.GET)
        User_ID = request.GET.get("User_ID",None)
        user = User.objects.get(User_ID=User_ID)
        user.delete()
        return Response({"msg":"Student Deleted"},status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        print(
        type(e).__name__,          # TypeError
        __file__,                  # /tmp/example.py
        e.__traceback__.tb_lineno  # 2
        )  
        return Response({"msg":"Something went wrong"},status=500)

@api_view(['GET'])
def student_list(request):
    try:
        page_no = int(request.GET.get("page_no",1))
        max_rows = int(request.GET.get("max_rows",10))
        user = User.objects.all()
        user = UserSerializer(user,many=True)
        from django.core.paginator import Paginator
        # p = Paginator(user,max_rows)
        # user = p.page(1)

        print(user.data)
        return Response({"users":user.data,"msg":"Success"},status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        print(
        type(e).__name__,          # TypeError
        __file__,                  # /tmp/example.py
        e.__traceback__.tb_lineno  # 2
        )   
        return Response({"msg":"Something went wrong"},status=500)
