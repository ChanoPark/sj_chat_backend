from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _ 

class UserManager(BaseUserManager): #User를 생성할때 쓰는 헬퍼클래스, 장고모델들은 Manager를 통해 쿼리셋을 받음
    def create_user(self, user_id, username, nickname,classnum, 
                    email, university, faculty, major, password=None, **extra_fields): # **extra_fields *이 2개면 나머지 값을 딕셔너리로 바꿔서 저장하고, 1개는 tuple로 저장한다.
        #이메일, 아이디, 닉네임, 비밀번호, 학번으로 User 인스턴스 생성 
        if not user_id:
            raise ValueError('Users must have an user_id') # rasie는 일부러 에러를 발생시키는 것이다.

        user = self.model(
            user_id = user_id,
            email = self.normalize_email(email),
            username = username,
            nickname = nickname,
            classnum = classnum,
            university = university,
            faculty = faculty,
            major = major,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, user_id, username, nickname, classnum, email, university, faculty, major, password=None, **extra_fields):
        user = self.create_user(
            user_id = user_id,
            username = username,
            password = password,
            nickname = nickname,
            classnum = classnum,
            email = email,
            university = university,
            faculty = faculty,
            major = major,
            is_superuser = True,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):  #실제 모델이 상속받아 생성하는 클래스
    objects = UserManager() 
    user_id = models.CharField(
        verbose_name ='user_id',
        max_length=16,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True
        )
    username = models.CharField(
        verbose_name='Username',
        max_length=10
        )
    nickname = models.CharField(
        verbose_name='Nickname',
        max_length=10, 
        unique=True
        )
    classnum = models.PositiveIntegerField(
        verbose_name='Classnum',
        unique=True
    )
    university = models.CharField(
        verbose_name='University',
        max_length=20
    )
    faculty = models.CharField(
        verbose_name='Faculty',
        max_length=30
    )
    major = models.CharField(
        verbose_name='Major',
        max_length=20
    )
    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True
    )
    is_admin = models.BooleanField(
        verbose_name='Is admin',
        default=False
    )

    USERNAME_FIELD = 'user_id'               #회원가입할때 입력하는 순서는 여기서 결정되는 듯
    REQUIRED_FIELDS = ['username','nickname', 'email', 'classnum', 'university', 'faculty', 'major' ]
#USERNAME_FIELD은 user model에서 사용할 고유 식별자로 필수로 입력해 주어야 한다. 
#REQUIRED_FIELDS 는 createsuperuser 커맨드를 실행하여 관리자를 생성할 때 입력받을 필드를 정의해주면 된다.
    @property
    def is_staff(self):
        return self.is_admin