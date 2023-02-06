from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
    
    def save(self, *args, **kwargs):
        created = self.pk is None
        super(User, self).save(*args, **kwargs)
        if created:
            Profile.objects.create_profile(self)



class ProfileManager(models.Manager):
    def create_profile(self, user):
        profile = self.create(user=user)
        return profile


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        default='default.jpg',
        upload_to='profile_pics',
    )

    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)
