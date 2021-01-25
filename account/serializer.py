from rest_framework import serializers
from django.contrib.auth.models import User

class UserShortcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id","username","email","nickname","classnum",'university','faculty','major')