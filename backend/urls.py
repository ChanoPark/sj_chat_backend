from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', obtain_jwt_token),    #jwt 로그인 뷰 함수 등록 obtain_jwt_token 유저정보를 반환
    path('auth/verify', verify_jwt_token),  #검증
    path('auth/resfresh', refresh_jwt_token),
    #path('user/', include('user.urls')), # 분할분할
    path('account/', include('account.urls')),
]