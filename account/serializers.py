from rest_framework import serializers
from account.models import AppUser, AdminUser

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('user_id', 'email', 'firstName', 'lastName', 'mobile',
        'is_active', 'created_date', 'is_admin', 'password')

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'