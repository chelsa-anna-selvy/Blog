from django.urls import path
from .views import (home, view_profile, add_blog, view_blog, edit_blog, 
                    blog_list, my_blogs, reset_password, user_logout,
                    edit_comment,delete_comment
                    )

app_name = 'userpanel'
urlpatterns=[
    path('', home, name='userhome'),
    path('view_profile/', view_profile, name='view_profile'),
    path('add_blog/', add_blog, name='add_blog'),
    path('view_blog/<int:blog_id>/', view_blog, name='view_blog'),
    path('edit_blog/<int:blog_id>/', edit_blog, name='edit_blog'),
    path('edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('my_blogs/', my_blogs, name='my_blogs'),
    path('blog_list/', blog_list, name='all_blog_list'),
    path('reset_password/', reset_password, name='user_reset_password'),
    path('logout/', user_logout, name='user_logout'),


]