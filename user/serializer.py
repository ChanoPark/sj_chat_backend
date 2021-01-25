#JSON에 모든 정보가 들어있는데 보안상 문제가 있을 수 있어서 이것을 사용
from rest_framework import serializers    #데이터를 보기 좋게 만들기 위함
from django.contrib.auth.models import User

class UserShortcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User   # Model 등록
        fields = ("username", "email", "first_name","last_name")
                #위 정보만 보이게 하기 위함













