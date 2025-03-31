from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(null=True, default= 'avatar.png' )
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Blogs(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    authors = models.ManyToManyField("Author")
    created = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    
    


class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    blogs = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body
    




