from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User
from .forms import UserAdmin


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)