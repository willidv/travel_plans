from __future__ import unicode_literals

from django.db import models



# Create your models here.

import re

NAMES_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')



# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        print postData
        errors = []
        if len(postData['name']) < 3:
            errors.append("Name should be longer than 2 characters")
        if len(postData['username']) < 3:
            errors.append('username should be longer than 2 characters')
        if not NAMES_REGEX.match(postData['name']):
            errors.append("Name must be letters only")
        if not NAMES_REGEX.match(postData['username']):
            errors.append("Username must be letters only")
        if postData['password'] != postData["confirm_password"]:
            errors.append("Passwords must match")
        return errors
    
    def login_validator(self, postData):
        error=[]
        username = postData['username']
        password = postData['password']

        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            user = None
        
        if user == None:
            error.append("You must be a registered user")
            return error
        else:
            if user.password != postData['password']:
                error.append("You must use the correct password")
                return error

class PlanManager(models.Manager):
    def travel_validator(self, postData):
        mistake = []
        t_d_from = postData["t_d_from"]
        t_d_to = postData["t_d_to"]
        destination = postData['destination']
        description = postData['description']

        if t_d_from >= t_d_to:
            mistake.append("You must leave before you come back")
            print mistake
            return mistake

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()
    def __str__(self):
        user_info = str(self.name) + " " + str(self.username)  
        return user_info

class Plan(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.TextField()
    t_d_from = models.DateField(auto_now=False)
    t_d_to = models.DateField(auto_now=False)
    travelers = models.ManyToManyField(User, related_name = "plans")