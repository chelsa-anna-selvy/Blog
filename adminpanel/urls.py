from django.urls import path
from .views import (home, user_list, view_user, blog_list, blog_view, 
                    reset_password, hide_blog, show_blog, activate_user, 
                    deactivate_user, userbased_blogs, hide_comment,show_comment,user_logout)

app_name = 'adminpanel'
urlpatterns=[
    path('', home, name='adminhome'),
    path('user_list/', user_list , name='user_list'),
    path('view_user/<int:user_id>/', view_user, name='view_user'),
    path('blog_list/', blog_list, name='blog_list'),
    path('blog_view/<int:blog_id>/', blog_view, name='blog_view'),
    path('hide_blog/<int:blog_id>/', hide_blog, name='hide_blog'),
    path('show_blog/<int:blog_id>/', show_blog, name='show_blog'),
    path('hide_comment/<int:comment_id>/', hide_comment, name='hide_comment'),
    path('show_comment/<int:comment_id>/', show_comment, name='show_comment'),
    path('activate_user/<int:user_id>/', activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', deactivate_user, name='deactivate_user'),
    path('user_blogs/<int:user_id>/', userbased_blogs, name='user_blogs'),
    path('reset_password/', reset_password, name='reset_password'),
    path('logout/', user_logout, name='user_logout'),
    
    
   
   
]