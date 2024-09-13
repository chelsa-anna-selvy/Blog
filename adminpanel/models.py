from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    phone = models.CharField(max_length=14)
    profile_image = models.ImageField(upload_to='profile_images/')
    id_proof = models.ImageField(upload_to='id_proof/')
    profile_description = models.TextField()
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    blog_image = models.ImageField(upload_to='blog_content/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    

    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog.title}'
    
