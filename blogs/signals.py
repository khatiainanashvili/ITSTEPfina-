from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from blogs.models import Author  


@receiver(post_save, sender=User)
def create_author_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance, name=instance.username)

@receiver(post_save, sender=User)
def save_author_profile(sender, instance, **kwargs):
    instance.author.save()
