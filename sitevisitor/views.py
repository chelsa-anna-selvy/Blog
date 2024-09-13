from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, LoginForm, OtpForm, ForgotPasswordForm, ProfileForm, SetNewPassword
from django.contrib import messages
from django.contrib.auth import authenticate,login
from adminpanel.models import Blog, User
from django.core.exceptions import ObjectDoesNotExist
# from .tasks import send_otp_task, send_welcome_mail_task
import random


# Create your views here.
def home(request):
    blogs = Blog.objects.filter(status='PUBLISH',user__is_active=True).order_by('-updated_at')
    
    context ={
        'blogs': blogs
    }
    return render(request,'sitevisitor/home.html',context)

def registration(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        form1 = ProfileForm(request.POST,request.FILES)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            profile = form1.save(commit = False)
            profile.user = user
            profile.save()
            # send_welcome_mail_task.delay(
            #     email=user.email,
            #     firstname=user.first_name,
            #     lastname=user.last_name
                
            # )
            messages.success(request,'You have registered successfully!!')
            return redirect('sitevisitor:sign_in')
    else:
        form = RegistrationForm()
        form1 = ProfileForm()
    return render(request,'sitevisitor/registration.html',{'form':form,'form1':form1})

def user_login(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username,password = password)
            if user is not None:
                login(request,user)
                if user.is_staff:
                    return redirect('adminpanel:adminhome')
                else:
                    return redirect('userpanel:userhome')
            else:
                messages.error(request,'Invalid username or password')

    else:
        form = LoginForm()
    return render(request,'sitevisitor/login.html',{'form':form})

def forgot_password(request):
  
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
                     
            try:
                is_user = User.objects.get(email=email, is_superuser=False, is_active=True, is_staff=False)
                request.session['email']  = email
                otp = random.randint(100000,999999)
                name = is_user.first_name+" "+ is_user.last_name            
            
            #     send_otp_task.delay(
            #     email=email,
            #     otp=otp,
            #     name=name,
            #     template_name='sitevisitor/email_message.html'
            # )
                
                
                return redirect('sitevisitor:otp',otp=otp)
            except ObjectDoesNotExist:
                messages.error(request, "Sorry!!! This email is not registered with us!!")
                return redirect('sitevisitor:sign_in')
    else:
        form = ForgotPasswordForm()

    return render(request,'sitevisitor/forgot_password.html',{'form':form})

def otp_generation(request,otp):
    if request.method =='POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            user_otp = form.cleaned_data.get('otp')
            if otp == user_otp:
                return redirect('sitevisitor:change_password')
            else:
                messages.error(request,'Invalid OTP. Try sending another one')
    
    else:
        form = OtpForm()
    return render(request,'sitevisitor/otp.html',{'form':form})

def reset_password(request):
    email = request.session.get('email', 'Guest')
    user = get_object_or_404(User,email = email)
    
    if request.method=='POST':
        form = SetNewPassword(user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Password Reset Successfully!!. Login to enjoy more services.')
            return redirect('sitevisitor:sign_in')
    else:
        form = SetNewPassword(user)
    return render(request,'sitevisitor/reset_password.html',{'form':form})

def unauthorized_access(request):
    return render(request,'sitevisitor/404.html')