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


from django.contrib.auth.models import User

class Books(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    authors = models.ManyToManyField("Author")

    def __str__(self):
        return self.title

    
    
def create_author_for_user(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance, name=instance.username)

@receiver(post_save, sender=User)

def save_author(sender, instance, **kwargs):
    if hasattr(instance, 'author'):
        instance.author.save()

class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    blogs = models.ForeignKey(Books, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body