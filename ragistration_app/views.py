
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
def ragistration_page(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        mob_number=request.POST.get('mob_number')
        
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        
        try:
            
            user_obj=User(username =username ,email = email)
            # if User.objects.filter(username==username):
            #     messages.success(request, 'Username is taken.')
            #     return redirect('/register')
            # if User.objects.filter(email = email):
            #     messages.success(request, 'Email is taken.')
            #     return redirect('/register')
            if password == confirm_password:
                user_obj.set_password(password)
            if len(mob_number)<10:
                messages.success(request,'Mobile number should be of 10 digits')
            else:
                messages.success(request, 'Both passwords are not matching')
            user_obj.save()
            auth_token=str(uuid.uuid4())
            profile_obj=Profile.objects.create(user=user_obj,auth_token=auth_token,mob_number=mob_number)
            profile_obj.save()
            send_email(email , auth_token)
            return redirect('token_send')
        except Exception as e:
            print(e)
    return render(request,'ragistration_form.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('login')
        
        login(request , user)
        return redirect('home')
    return render(request,"loginform.html")

def success_page(request):
    return render(request,'success.html')

def token_send(request):
    return render(request,'token_send.html')

def home(request):
    return render(request,'Home.html')

def send_email(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def verify_email(request,auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,'Your account is already verified.')
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Your account is verified.')
            return redirect('login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')
    
def error_page(request):
    return render(request,'error.html')