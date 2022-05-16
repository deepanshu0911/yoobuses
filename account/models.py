from django.db import models
import uuid
import os
from django.contrib.auth.hashers import make_password, check_password
 
class AppUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    firstName = models.CharField(max_length=100, default="Unknown user")
    lastName = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=1000, null=True, blank=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.email + ' - ' + self.firstName

class AdminUser(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=1000, default=None)
    objects = models.Manager()

    def save(self, *args, **kwargs):
       self.password = make_password(self.password)
       super(AdminUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username   
    