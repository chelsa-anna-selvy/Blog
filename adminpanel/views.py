from django.shortcuts import render, redirect, get_object_or_404
from userpanel.forms import BlogForm, CommentForm, ChangePasswordForm, RegistrationForm, ProfileForm
from .models import User, Profile, Blog, Comment
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# from sitevisitor.tasks import update_status_mail_task

# Create your views here.

@login_required(login_url='/404/')
def home(request):
    logged_user = request.user
    blog_count = Blog.objects.exclude(status ='DRAFT').count()
    published_blog_count =Blog.objects.filter(status='PUBLISH').count()
    user_count = User.objects.filter(is_staff = False).count()
    active_user_count = User.objects.filter(is_active = True, is_staff = False).count()
    context ={
        'logged_user':logged_user,
        'blog_count':blog_count,
        'published_blog_count':published_blog_count,
        'user_count':user_count,
        'active_user_count':active_user_count,

    }
    return render(request,'adminpanel/admin_home.html',context)


@login_required(login_url='/404/')
def user_list(request):
    logged_user = request.user
    all_users = Profile.objects.exclude(user__is_staff=True)
    active_users =Profile.objects.filter(user__is_active=True,user__is_staff=False)
    inactive_users =Profile.objects.filter(user__is_active=False,user__is_staff=False)
    context={
        'logged_user':logged_user,
        'all_users':all_users,
        'active_users':active_users,
        'inactive_users': inactive_users,
        'count':all_users.count()
    }
    return render(request,'adminpanel/user_list.html',context)


@login_required(login_url='/404/')
def view_user(request,user_id):
    user = get_object_or_404(User, id = user_id)
    profile =get_object_or_404(Profile, user = user)
    
    context = {
        'user':user,
        'profile': profile,
        
    }
    return render(request,'adminpanel/view_user.html',context)


@login_required(login_url='/404/')
def activate_user(request,user_id):
    user =get_object_or_404(User, id = user_id)
    if request.method =='POST':
        user.is_active = True
        user.save()
        # update_status_mail_task.delay(
        #         email=user.email,
        #         firstname=user.first_name,
        #         lastname=user.last_name,
        #         status='activated',
        #         username = user.username,
                
        #     )
        messages.success(request,'User activated successfully')
    return redirect('adminpanel:user_list')


@login_required(login_url='/404/')
def deactivate_user(request,user_id):
    user =get_object_or_404(User, id = user_id)
    if request.method =='POST':
        user.is_active = False
        user.save()
        # update_status_mail_task.delay(
        #         email=user.email,
        #         firstname=user.first_name,
        #         lastname=user.last_name,
        #         status='deactivated',
        #         username = user.username,
                
        #     )
        messages.success(request,'User deactivated successfully')
    return redirect('adminpanel:user_list')

@login_required(login_url='/404/')
def userbased_blogs(request, user_id):    
    user = get_object_or_404(User, id= user_id)
    profile= get_object_or_404(Profile,user= user)
    published_blogs = Blog.objects.filter(user = user, status ='PUBLISH')
    hidden_blogs =  Blog.objects.filter(user = user, status ='HIDDEN')
    blogs = Blog.objects.filter(user = user).exclude(status='DRAFT')
    count = blogs.count()
    context = {
        'user':user,
        'profile': profile,
        'published_blogs': published_blogs,
        'hidden_blogs': hidden_blogs,
        'blogs' : blogs,
        'count':count
    }
    return render(request,'adminpanel/view_user_blogs.html', context)


@login_required(login_url='/404/')
def blog_list(request):
    logged_user =request.user
    blogs = Blog.objects.exclude(status ='DRAFT')
    context = {
        'logged_user':logged_user,
        'blogs': blogs
    }
    return render(request,'adminpanel/blog_list.html', context)


@login_required(login_url='/404/')
def blog_view(request, blog_id):
    blog = get_object_or_404(Blog, id = blog_id)
    comments = Comment.objects.filter(blog = blog)    
    logged_user = request.user
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
            return redirect(blog_view, blog_id = blog.id)
    else:
        form = CommentForm()
    count = comments.count()
    context = {
        'logged_user':logged_user,
        'form':form,
        'blog':blog,
        'comments':comments,        
        'count': count
    }
    return render(request,'adminpanel/blog_view.html', context)

@login_required(login_url='/404/')
def reset_password(request):

    # form = ChangePasswordForm(user= request.user)
    return render(request,'adminpanel/reset_password.html')

@login_required(login_url='/404/')
def hide_blog(request,blog_id):
    logged_user = request.user
    blog =get_object_or_404(Blog,id = blog_id )
    if request.method =='POST':
        blog.status ='HIDDEN'
        blog.save()
        messages.success(request, 'The blog is hidden from general public!!!')
        
    return redirect('adminpanel:adminhome')

@login_required(login_url='/404/')
def show_blog(request,blog_id):
    logged_user = request.user
    blog =get_object_or_404(Blog,id = blog_id )
    if request.method =='POST':
        blog.status ='PUBLISH'
        blog.save()
        messages.success(request, 'Now the blog is visible to everyone!!!')

    return redirect('adminpanel:adminhome')   

@login_required(login_url='/404/')
def show_comment(request,comment_id):
    logged_user = request.user
    comment =get_object_or_404(Comment,id = comment_id )
    blog_id = comment.blog.id
    if request.method =='POST':
        comment.status ='SHOW'
        comment.save()
        messages.success(request, 'Now the comment is visible to everyone!!!')
    
    return redirect('adminpanel:blog_view',blog_id = blog_id)

@login_required(login_url='/404/')
def hide_comment(request,comment_id):
    logged_user = request.user
    comment =get_object_or_404(Comment,id = comment_id )
    blog_id = comment.blog.id
    if request.method =='POST':
        comment.status ='HIDDEN'
        comment.save()
        messages.success(request, 'The comment is hidden from general public!!!')
        
    return redirect('adminpanel:blog_view',blog_id = blog_id)

@login_required(login_url='/404/')
def reset_password(request):
    logged_user=request.user
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Password updated successfully. Login again to enjoy the services!!')
            return redirect('adminpanel:home') 
    else:
        form = ChangePasswordForm(user=request.user)
    context = {
        'logged_user':logged_user,
        'form':form
    }
    return render(request, 'adminpanel/reset_password.html', context)

@login_required(login_url='/404/')
def user_logout(request):    
    logout(request)
    return redirect('sitevisitor:home')

