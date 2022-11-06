from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from app.serializers import *
# import django.contrib.auth.context_processors.csrf
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required

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
        # username = request.data.get('username',None)
        address = request.data.get('address',None)
        phone = request.data.get('phone',None)
        is_admin = request.data.get('is_admin',False)

        if not password or not email:
            return Response({"mesg":"Please Enter all details"},status=status.HTTP_400_BAD_REQUEST) 
        if User.objects.filter(email=email).exists():
            return Response({"mesg":"Email Already exists"},status=status.HTTP_400_BAD_REQUEST) 

        user = User.objects.create(username=email,email=email,first_name=first_name,last_name=last_name,phone=phone,address=address, is_admin=is_admin)
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
        email = request.data.get('email',None)
        if not password or not email:
            return Response({"mesg":"Please Enter credentials"},status=status.HTTP_400_BAD_REQUEST) 

        user = authenticate(request,username=email,password=password)
        print(user.session_token)
        if int(user.session_token):
            return Response({"mesg":"Already logged in"}, status=status.HTTP_200_OK)
        if user:
            login(request,user)
            user.session_token=str(user.User_ID)
            user.save()
            print(user.session_token)

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
        user_id = request.GET.get("user_id",None)
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

        user = User.objects.get(User_ID=int(User_ID))
        if not int(user.session_token):
            return Response({"msg":"Please Login"},status=403)
        print(int(user_id) == user.User_ID,user.User_ID,user_id,is_admin)
        if is_admin: 
            print("admin", type(is_admin))
            if first_name:
                user.first_name=first_name
            if last_name:
                user.last_name=last_name
            if password:
                user.set_password(password)
            if address:
                print()
                user.address=address
            if phone:
                user.phone=phone
            user.save()
            return Response({"msg":"Student Updated"},status=status.HTTP_200_OK)
        elif int(user_id) == user.User_ID:
            print("reg")
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
        else:
            return Response({"msg":"You are not authorized"},status=403)

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

# @login_required
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
        # print(request.user.User_ID)
        # u = User.objects.get(username=request.user)
        # print(u.email)
        return Response({"users":user.data,"msg":"Success"},status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        print(
        type(e).__name__,          # TypeError
        __file__,                  # /tmp/example.py
        e.__traceback__.tb_lineno  # 2
        )   
        return Response({"msg":"Something went wrong"},status=500)

from django.contrib.auth import logout

@api_view(['GET'])
def logout_view(request):
    user_id = request.GET.get("user_id",None)
    user = User.objects.get(User_ID=int(user_id))
    user.session_token=0
    user.save()
    logout(request)
    return Response({"msg":"Logout Success"},status=status.HTTP_200_OK)
