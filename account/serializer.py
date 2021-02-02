from rest_framework import serializers
from .models import User

class UserShortcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id","username","email","nickname","university","faculty","major","classnum")
        