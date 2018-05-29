
from django.shortcuts import render,redirect,HttpResponse
from models import User,Wish
import bcrypt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages


def index(request):
    return render(request,'wishlist/index.html')


def register(request):
    User.objects.validate(request)
    return redirect('/')


def login(request):
    if request.method == "POST":
       username = request.POST['username']
       password = request.POST['password']
        
    for key in request.POST:
            if request.POST[key] == "":
                messages.error(request,"Please enter all inputs")
                return redirect('/')

    user = User.objects.filter(username=username)
    if len(user) > 0:
		        # if user exists, check password
        isPassword = bcrypt.checkpw(password.encode(), user[0].password.encode())
        if isPassword:
            request.session['id'] = user[0].id
            return redirect('/dashboard')
        else:
            messages.error(request, "Incorrect username/password combination.")
            return redirect('/')
    else:
        messages.error(request, "User does not exist. Please Register first!")
        return redirect('/')

	               

def logout(request):
    request.session.clear()
    return redirect('/')


def dashboard(request):
    user = User.objects.get(id=request.session['id'])
    user_wish_list = Wish.objects.filter(users=user)
    others_wish_list = Wish.objects.exclude(users=user)
    context={
            'user':user,
            'user_wish_list':user_wish_list,
            'others_wish_list':others_wish_list 
    }
    return render(request,'wishlist/dashboard.html',context)


def add_wish(request):
    return render(request,'wishlist/add_wish.html')


def addwish(request):
    valid = Wish.objects.validate_product(request)
    if valid:
        return redirect('/dashboard')
    return redirect('/add_wish')


def add_to_mywish_too(request,wish_id):
    new_wish =Wish.objects.get(id=wish_id)
    user = User.objects.get(id = request.session['id'])
    new_wish.users.add(user)
    return redirect('/dashboard')


def remove_from_mywish(request,wish_id):
    rem_wish =Wish.objects.get(id=wish_id)
    user = User.objects.get(id = request.session['id'])
    rem_wish.users.remove(user)
    return redirect('/dashboard')

def delete_from_mywish(request,wish_id):
    del_wish = Wish.objects.get(id=wish_id)
    #user = User.objects.get(id = request.session['id'])
    del_wish.delete()
    #user.wishes.remove(del_wish)
    return redirect('/dashboard')

def item_wished_by(request,item_id):
    item_details = Wish.objects.get(id=item_id)
    whose_wish = User.objects.filter(wishes=item_details) 
    context={
        'item_details':item_details,
        'whose_wish':whose_wish
    }
   
    return render(request,'wishlist/item_wished.html',context)




