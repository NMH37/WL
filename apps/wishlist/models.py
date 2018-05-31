


from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import bcrypt
#from django.core.validators import validate_email
#from django.core.exceptions import ValidationError

# Create your models here.


class UserManager(models.Manager):
    def validate(self,request):
        if request.method == "POST":
            valid = True
            for key in request.POST:
                if request.POST[key] == "":
                    messages.error(request,"Please enter {}".format(key))
                    valid = False
                    return valid
            name=request.POST['name']
            username=request.POST['username']
            password = request.POST['password']
                    
            if len(username)<3 and len(name) <3:
                valid= False
                messages.error(request,"Must be atleast 3 characters in name/username")
            if len(request.POST['password'])< 8 and not(password.isalpha()):
                valid = False
                messages.error(request,"password must have 8 characters including atleast one alphabet")


            if request.POST['confirmpassword']!= request.POST['password']:
                valid = False
                messages.error(request,"password doesn't match")

            if valid == True:
                # encrypt password 
                password = request.POST['password']
                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())		
                User.objects.create(name=request.POST['name'],username=request.POST['username'],password=hashed_pw,hired=request.POST['hired_date'] )
                messages.success(request,"Successfully Registered, Proceed to login")
                return valid


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    hired = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __str__(self):
        return "Name: {},Username: {}".format(self.name,self.username)


class ProductManager(models.Manager):
    def validate_product(self,request):
        if request.method == "POST":
            valid = True
            for key in request.POST:
                if request.POST[key] == "" or len(request.POST[key])< 3 :
                    messages.error(request,"Please fill the product field, at least 3 characters long ")
                    valid = False
                    return valid
                
                else:
                    valid = True
                    product_name = request.POST['item'] 
                    user= User.objects.get(id=request.session['id'])
                    wish=Wish.objects.create(item = product_name,added_by=user.username)
                    wish.users.add(user)
                    return valid




class Wish(models.Model):
    item = models.CharField(max_length= 255)
    added_by = models.CharField(max_length= 255)
    users = models.ManyToManyField(User,related_name='wishes')
    created_at = models.DateTimeField(auto_now_add = True)

    objects = ProductManager()

    def __str__(self):
        return "Item: {}, Added by:{}".format(self.item,self.added_by)