from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from account.models import AppUser, AdminUser
from account.serializers import AppUserSerializer, AdminUserSerializer

@csrf_exempt
def userCreate(request):
    if request.method == "POST":
     data = JSONParser().parse(request)
     if not AppUser.objects.filter(email=data['email']).exists():
         user = AppUser.objects.create(firstName=data['name'],email=data['email'])
         user.password = make_password(data['password'])
         user.save()
         return JsonResponse({'status': 'created'}, safe="False")
     else:
        return JsonResponse({'status': 'exists'}, safe="False")                

@csrf_exempt
def updateUser(request):
  if request.method == 'POST':
      data = JSONParser().parse(request)
      if AppUser.objects.filter(email=data['email']).exists():
          AppUser.objects.filter(email=data['email']).update(firstName=data['firstName'],
          email=data['email'], mobile=data['mobile'])
          return JsonResponse({'status': 'success'})


def printUsers(request):
  if request.method=="GET":
      users = AppUser.objects.all().order_by('-user_id')[:5]
      usersData = AppUserSerializer(users, many=True)
      return JsonResponse({'status': 'success', 'result': usersData.data}, safe=False)

@csrf_exempt
def deleteUser(request):
    if request.method=="POST":
        data = JSONParser().parse(request)
        try:
          AppUser.objects.filter(user_id=data['user_id']).delete()
          return JsonResponse({'status': 'success'})
        except:
          return JsonResponse({'status': 'failed'})

@csrf_exempt
def userLogin(request):
    if request.method == "POST":
     data = JSONParser().parse(request)
     if AppUser.objects.filter(email=data['email']).exists():
        user = AppUser.objects.get(email=data['email'])
        loginPassword = data['password']
        check = check_password(loginPassword, user.password)
        if check:
            userObject = AppUser.objects.filter(email=data['email'])
            userData = AppUserSerializer(userObject, many=True)
            return JsonResponse({'user': userData.data, 'status': 'found'}, safe=False)
        else:
            return JsonResponse({'status': 'wrong-password'}, safe=False)
     else:
        return JsonResponse({'status': 'not-found'}, safe=False)

@csrf_exempt
def adminLogin(request):
    if request.method == "POST":
     data = JSONParser().parse(request)
     if AdminUser.objects.filter(username=data['username']).exists():
        admin = AdminUser.objects.get(username=data['username'])
        loginPassword = data['password']
        check = check_password(loginPassword, admin.password)
        if check:
            userObject = AdminUser.objects.filter(username=data['username'])
            userData = AdminUserSerializer(userObject, many=True)
            return JsonResponse({'user': userData.data, 'status': 'found'}, safe=False)
        else:
            return JsonResponse({'status': 'wrong-password'}, safe=False)
     else:
        return JsonResponse({'status': 'not-found'}, safe=False)



