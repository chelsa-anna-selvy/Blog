from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogForm, CommentForm, ChangePasswordForm, RegistrationForm, ProfileForm
from adminpanel.models import User, Profile, Blog, Comment
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/404/')
def logged_user_data(request):
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)
    return logged_user, profile


@login_required(login_url='/404/')
def home(request):
    logged_user, profile = logged_user_data(request)
    context = {
        'logged_user':logged_user,
        'profile': profile
    }
    return render(request,'userpanel/user_home.html', context)

@login_required(login_url='/404/')
def view_profile(request):
    logged_user, profile = logged_user_data(request)
    if request.method =='POST':
        form = RegistrationForm(request.POST, instance = logged_user)
        form1 = ProfileForm(request.POST, request.FILES,instance = profile)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            messages.success(request,'Profile Updated Successfully!!')
            return redirect('userpanel:view_profile')
    else:
        form = RegistrationForm(instance = logged_user)
        form1 = ProfileForm(instance = profile)
    context = {
        'logged_user':logged_user,
        'profile': profile,
        'form': form,
        'form1': form1
    }
    return render(request,'userpanel/view_profile.html', context)


@login_required(login_url='/404/')
def add_blog(request):
    logged_user, profile = logged_user_data(request)
    if request.method == 'POST':
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid:
            blog = form.save(commit =False)
            blog.user = logged_user
            blog.created_at = timezone.now()
            blog.updated_at = timezone.now()
            blog.save()
            messages.success(request,'A new blog is created successfully!!')
            return redirect('userpanel:my_blogs')
    else:        
        form = BlogForm()
    
    context = {
        'logged_user':logged_user,
        'profile': profile,
        'form':form
    }
    return render(request,'userpanel/add_blog.html', context)


@login_required(login_url='/404/')
def view_blog(request, blog_id):
    blog = get_object_or_404(Blog, id = blog_id)
    comments = Comment.objects.filter(blog = blog, status='SHOW')    
    logged_user, profile = logged_user_data(request)
    if request.method =='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.author =logged_user
            comment.created_at = timezone.now()
            comment.updated_at = timezone.now()
            comment.status ='SHOW'
            comment.blog = blog
            comment.save()
            return redirect('userpanel:view_blog', blog_id = blog.id)
    else:
        form = CommentForm()
    count = comments.count()
    context = {
        'logged_user':logged_user,
        'profile': profile,
        'form':form,
        'blog':blog,
        'comments':comments,        
        'count': count
    }
    return render(request,'userpanel/view_blog.html', context)


@login_required(login_url='/404/')
def edit_blog(request, blog_id):
    selected_blog = get_object_or_404(Blog, id = blog_id)
    logged_user, profile = logged_user_data(request)
    if request.method == 'POST':
        form = BlogForm(request.POST,request.FILES, instance = selected_blog)
        if form.is_valid:
            blog = form.save(commit =False)
            blog.user = logged_user
            blog.updated_at = timezone.now()
            blog.save()
            messages.success(request,'The blog is updated successfully!!')
            return redirect('userpanel:my_blogs')
    else:        
        form = BlogForm(instance = selected_blog)
    
    context = {
        'logged_user':logged_user,
        'profile': profile,
        'form':form
    }
    return render(request,'userpanel/edit_blog.html', context)


@login_required(login_url='/404/')
def blog_list(request):
    logged_user, profile = logged_user_data(request)
    blogs = Blog.objects.filter(status ='PUBLISH',user__is_active = True)
    context = {
        'logged_user':logged_user,
        'profile': profile,
        'blogs': blogs
    }
    return render(request,'userpanel/blog_list.html', context)


@login_required(login_url='/404/')
def my_blogs(request):
   
    logged_user, profile = logged_user_data(request)
    published_blogs = Blog.objects.filter(user = logged_user, status ='PUBLISH')
    drafted_blogs =  Blog.objects.filter(user = logged_user, status ='DRAFT')
    blogs = Blog.objects.filter(user = logged_user).exclude(status ='HIDDEN')
    # blogs = my_blogs.exclude(status = 'HIDDEN')
    count = blogs.count()
    context = {
        'logged_user':logged_user,
        'profile': profile,
        'published_blogs': published_blogs,
        'drafted_blogs': drafted_blogs,
        'blogs' : blogs,
        'count':count
    }
    return render(request,'userpanel/my_blogs.html', context)


@login_required(login_url='/404/')
def reset_password(request):
    logged_user, profile = logged_user_data(request)
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Password updated successfully. Login again to enjoy the services!!')
            return redirect('userpanel:userhome') 
    else:
        form = ChangePasswordForm(user=request.user)
    context = {
        'logged_user':logged_user,
        'profile': profile,
        'form':form
    }
    return render(request, 'userpanel/reset_password.html', context)


@login_required(login_url ='/404/')
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id = comment_id)
    blog = get_object_or_404(Blog, id = comment.blog.id)
    comments = Comment.objects.filter(blog = blog, status='SHOW')    
    logged_user, profile = logged_user_data(request)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance = comment)
        if form.is_valid():
            form.save()
            messages.success(request,'Comment Updated Successfully!!!')
            return redirect('userpanel:view_blog', blog_id = comment.blog.id)            
    else:
        form = CommentForm(instance = comment)
    count = comments.count()
    context = {
        'logged_user':logged_user,
        'profile': profile,
        'form':form,
        'blog':blog,
        'comments':comments,        
        'count': count
    }
    
    return render(request,'userpanel/view_blog.html', context)
    

@login_required(login_url ='/404/')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id = comment_id)
    if request.method == 'POST':
        comment.delete()
        messages.success(request,'Comment Deleted Successfully!!!')            
    
    return redirect('userpanel:view_blog', blog_id = comment.blog.id)
        

@login_required(login_url='/404/')
def user_logout(request):    
    logout(request)
    return redirect('sitevisitor:home')