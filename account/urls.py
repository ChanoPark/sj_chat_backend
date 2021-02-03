from django.urls import path
from account import views

urlpatterns =[
    path('register/', views.register),
    path('info/',views.info),
    path('del/',views.user_delete),
    path('changepw/',views.change_password),
    path('logout/',views.user_logout),
]