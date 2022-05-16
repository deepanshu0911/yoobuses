from django.urls import path
from account import views

urlpatterns = [
    path('create-user', views.userCreate, name="create-user"),
    path('update-user', views.updateUser),
    path('print-users', views.printUsers, name="print-users"),
    path('delete-user', views.deleteUser, name="delete-user"),

    path('user-login', views.userLogin, name="user-login"),
    path('admin-login', views.adminLogin),
]