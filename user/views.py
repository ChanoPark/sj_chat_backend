from django.contrib.auth.models import User #기본유저모델
from django.forms.models import model_to_dict #모델을 딕셔너리형태로 반환
from rest_framework import status 
from rest_framework.response import Response # json형태로 반환하기 위함
from rest_framework.decorators import api_view, permission_classes, authentication_classes
#api_view: 어떤 메소드 형태로 들어왔는지, json을 딕셔너리 형태로 만듬
#permission_classes: 로그인한 유저만 들어올지말지 / 3번째는 이유모름
from rest_framework.permissions import IsAuthenticated #로그인 했는지 안했는지
from user.serializer import UserShortcutSerializer


@api_view(['POST'])               #무조건 POST 형식으로만 받는다. put,delete,get방식으로 안받기위해
def register(request):           #request 어디서,어떤 정보가 왔는지에 대한 객체
    data = request.data           #딕셔너리형태로 들어가있음
    required_fields = ('username', 'password', 'first_name','last_name', 'email' ) #회원가입시 필요한 필드, 필요한 정보가 다 들어있는지
    if all(i in data for i in required_fields):              #required_필드에 있는 데이터가 모두 있으면 true
        user_check = User.objects.filter(username=data['username'])              #아이디 중복 확인
        email_check = User.objects.filter(email=data['email'])               #이메일 중복확인
        if user_check.exists():          #중복 아이디 존재시 
            return Response({"message" : "아이디가 존재합니다."}, status=status.HTTP_409_CONFLICT) #리스폰스 딕셔너리 형태로 반환
        elif email_check.exists():
            return Response({"message":"이메일이 존재합니다."}, status = status.HTTP_409_CONFLICT)
        else: #이제 회원가입 시켜줌
            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password'],
            )
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()
            return Response(model_to_dict(user), status=status.HTTP_201_CREATED) #유저를 딕셔너리로 만들어서 반환 
    else:  #필드 검증 실패
        return Response({"message": "key error"}, status=status.HTTP_BAD_REQUEST)


@api_view(['GET']) #특정 메소드로만 요청을 받게 한다
@permission_classes((IsAuthenticated,)) #로그인 되었을 경우만 뷰함수 실행, 로그인 안했으면 401을 뱉음 / 이터레이티브가 들어감
def my_profile(request):            #내 정보 가져오기
    user = request.user
    serializer = UserShortcutSerializer(user) #값이 여러개면 (user, many=true) 하면됌 / 이건 원하는 값을 필터링
    return Response(serializer.data, status=status.HTTP_200_OK)
