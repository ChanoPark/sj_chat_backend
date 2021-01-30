from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json  #json.loads는 json형태의 데이터를 딕셔너리로 바꿈
from django.contrib.auth.hashers import check_password
from .models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from account.serializer import UserShortcutSerializer
from django.forms.models import model_to_dict
import re

from django.contrib.auth.forms import PasswordChangeForm


def user_validation(data):
    user_check = User.objects.filter(user_id=data['user_id']) #아이디 체크
    email_check1 = re.compile(
        r'[0-9a-zA-Z]+@[0-9a-zA-Z]+\.[0-9a-zA-Z]{2,}'
    ).search(data['email']) #이메일 정규표현식
    email_check2 = User.objects.filter(email=data['email']) #이메일 중복체크

    if user_check.exists():
        return "USER_EXIST"
    elif email_check1 is None:
        return "EMAIL_INVALID"
    elif email_check2.exists():
        return "EMAIL_EXIST"
    else:
        return "OK"

@api_view(['POST'])
def register(request):
    data = json.loads(request.body)
    required_fields = ('user_id','username','nickname','email','classnum','password','university','faculty','major')
    
    # JSON 필드 체크
    if not all(i in data for i in required_fields):
        return Response(
            {"message":"필수 양식을 입력해주세요."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    validation = user_validation(data)

    if validation == "USER_EXIST":
        return Response(
            {"message":"이미 존재하는 아이디입니다."},
            status=status.HTTP_409_CONFLICT
        )
    elif validation == "EMAIL_INVALID":
        return Response(
            {"message":"정확한 이메일 형식을 입력해주세요."},
            status=status.HTTP_400_BAD_REQUEST
        )
    elif validation == "EMAIL_EXIST":
        return Response(
            {"message":"이미 존재하는 이메일입니다."},
            status = status.HTTP_409_CONFLICT
        )
    else:
        user = User.objects.create_user(**data)
        return Response(
            model_to_dict(user),
            status=status.HTTP_201_CREATED
        )
"""
학번도 유니코드임 -> 17,18학번 이렇게 입력할꺼면 DB수정해야됌
그대로 2017270920 이렇게 받을꺼면 validation에서 중복되면 에러메세지뜨게 해야함.
"""

@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,)) #( ~,) 형태로 있으면 튜플
def info(request):
    user = request.user   #오브젝트에 들어있는 속성들
    data = request.data   #PUT으로 들어온 데이터들
    email = request.user.email
    classnum = request.user.classnum
    nickname= request.user.nickname

    if request.method == "GET": #사용자 정보 반환
        result = UserShortcutSerializer(user)
        return Response(result.data, status=status.HTTP_200_OK)
    else:

        
        required_field = ('password')     #   Q. 회원정보 수정하는데 꼭 어떤 정보가 들어와야할까? 
                                          #   A. 아무나 정보를 바꾸는 것을 방지하기 위해 비밀번호는 확인하는걸로
        #if not all(i in data for i in required_field):
        if not required_field:       
            return Response(
                {"message":"필수 양식을 입력해주세요"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
                  
        email_check1 = re.compile(
                r'[0-9a-zA-Z]+@[0-9a-zA-Z]+\.[0-9a-zA-Z]{2,}'            # 이메일 정규 표현식
        ).search(data['email'])
        email_check2 = User.objects.filter(email=data['email'])          # 이메일 중복 체크
        classnum_check = User.objects.filter(classnum=data['classnum'])  #학번 중복 체크
        nickname_check = User.objects.filter(nickname=data['nickname'])  #별명 중복 체크

        if not check_password:  #check_password로 변경
            return Response(
                {"message":"비밀번호를 확인해주세요"},
                status=status.HTTP_403_FORBIDDEN
            )
        elif email_check1 is None:
            return Response(
                {"Message":"정확한 이메일 형식을 입력해주세요"},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif email_check2.exists() and email != data['email']:
            return Response(
                {"message":"이미 존재하는 이메일입니다."},
                status=status.HTTP_409_CONFLICT
            )
        elif classnum_check.exists() and classnum != data['classnum']:
            return Response(
                {"message":"이미 존재하는 학번입니다."},
                status=status.HTTP_409_CONFLICT
            )
        elif nickname_check.exists() and nickname != data['nickname']:
            return Response(
                {"message":"이미 존재하는 별명입니다."},
                status=status.HTTP_409_CONFLICT
            )
        else:
            not_allowed = [       #변경되면 안되는 정보들은 걸러냄
                'password', 'last_login', 'user_id',
                'is_active', 'is_admin'
            ]
            #변경되는 안되는 정보들 객체에 들어가기 전에 data에서 삭제
            for n in not_allowed:
                if n in data:
                    del data[n]
            
            #user 객체에 assign
            for attr, value in data.items():
                setattr(user, attr, value)   #객체 속성변경
            
            user.save()
            return Response(
                UserShortcutSerializer(user).data,
                status=status.HTTP_202_ACCEPTED
            )


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def change_password(request):
    user = request.user
    data = request.data

    required_field = ('current_password', ' new_password1', 'new_password2')

    if not all(i in data for i in required_field):
        return Response(
            {"message":"필수 양식을 입력해주세요."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not check_password(data['current_password'], user.password):  #현재 비밀번호 확인
        return Response(
            {"message":"필수 양식을 입력해주세요."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    elif data['new_password1'] != data['new_password2']:
        return Response(
            {"message":"새 비밀번호가 일치하지 않습니다."},
            status=status.HTTP_400_BAD_REQUEST
        )
    else: #변경
        user.set_password(data['new_password1'])
        user.save()
        return Response(
            {"message":"비밀번호가 성공적으로 변경되었습니다."},
            status=status.HTTP_202_ACCEPTED
        )

"""
@api_view(['GET'])
def header_info(request):
    is_authenticated = request.user.is_authenticated() #로그인 확인
    user = request.user

    if not is_authenticated:
        return Response(
            {"message":"Not Logged in"},
            status = status.HTTP_204_NO_CONTENT
        )

    data = {
        "user_id" : user.user_id,
        "username" : user.username,
        "nickname" : user.nickname,
        "email" : user.email,
        "university":user.university,
        "faculty":user.faculty,
        "major":user.major,
        "classnum" : user.classnum,
    }

    return Response(data, status=status.HTTP_200_OK)

"""
"""
@api_view(['GET'])
@permission_classes((IsAuthenticated,)) 
def user_profile(request, user_id):       #다른사람 유저정보 확인
    user = request.user
    
    try:
        user = User.objects.get(user_id=user_id)
        data = {
            "classnum":user.classnum,
            "user_id":user.user_id,
            "username":user.username,
            "nickname":user.nickname,
            "email":user.email,
            "university":user.university,
            "faculty":user.faculty,
            "major":user.major
        }
        return Response(data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {"message":"User not exist"},
            status=status.HTTP_404_NOT_FOUND
        )
"""
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def user_delete(request):
    data = request.data
    user_check = User.objects.filter(user_id=data['user_id'])

    if not user_check.exists():
        return Response(
            {"message":"아이디가 일치하지 않습니다."},
            status=status.HTTP_409_CONFLICT
        )
    else:
        user = request.user
        user.delete()
        return Response(
            {"message":"회원탈퇴가 완료되었습니다."},
            status=status.HTTP_200_OK
        )