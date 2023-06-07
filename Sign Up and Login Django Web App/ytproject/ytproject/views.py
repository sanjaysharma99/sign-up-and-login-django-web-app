from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
        return redirect('/account/')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')

            user=User.objects.filter(username=username)

            if user.exists():
                messages.info(request,'Username Already Exists')
                return redirect('/')
            
            user=User.objects.create(username=username,email=email)
            user.set_password(password)
            user.save()

            messages.info(request,'Account Created Successfully')
            return redirect('/')
        
        return render(request,'registration.html')
    
def userlogin(request):
    if request.user.is_authenticated:
        return redirect('/account/')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            if not User.objects.filter(username=username).exists():
                messages.info(request,'Account Not Found')
                return redirect('/login/')
            
            user=authenticate(username=username,password=password)

            if user is None:
                messages.info(request,'Invalid Information')
                return redirect('/login/')
            else:
                login(request,user)
                return redirect('/account/')
        
        return render(request,'login.html')
    
@login_required(login_url='/login/')
def account(request):
    user=request.user.username
    return render(request,'account.html',{'username':user})

def userlogout(request):
    logout(request)
    return redirect('/login')