#forms은 어드민 사이트를 위한 파일이다. 
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User

class UserCreationForm(forms.ModelForm):
    #유저 생성 폼
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput) # 비밀번호 입력시 *로 표현하게 함
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_id','username', 'nickname', 'classnum','email','university','faculty','major')

    def clean_password2(self):
        #일치확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 일치하지 않습니다.")
        return password2
    
    def save(self, commit=True):
        #저장
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    #유저정보변경
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'user_id','username', 'nickname','classnum','email','is_admin','is_active',
            'university', 'faculty', 'major'
        )
    
    def clean_password(self):
        return self.initail["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'user_id','username', 'nickname', 'classnum', 'email',
        'university', 'faculty', 'major','is_admin','is_active'
    )
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('user_id', 'password')}),
        ('Personal info', {'fields': (
            'username', 'nickname', 'classnum', 'email',
            'university', 'faculty', 'major'
        )}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'user_type')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields' : ('user_id','username', 'nickname', 'email', 'password1','password2','classnum',
                        'university', 'faculty', 'major'),
        }),
    )

    search_fields = ('classnum', 'username',)
    ordering = ('classnum', 'username',)
    filter_horizontal = ()