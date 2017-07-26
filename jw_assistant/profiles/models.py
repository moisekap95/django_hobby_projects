from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse # For update and create views
from congregations.models import Congregation
from django.db.models.signals import post_save  #is emitted by django whenever a model instance gets saved to the database
from django.dispatch import receiver #Decorator

import os.path

#@receiver(post_save, sender=User)
#def ensure_profile_exists(sender, **kwargs):
    #if kwargs.get('created', False):
        #UserProfile.objects.get_or_create(user=kwargs.get('instance'))

# PROFILES MODELS
# Create your models here.
class UserProfile(models.Model):

    # Create relationship to extend the build in User Model (don't inherit from User!)
    user = models.OneToOneField(User, related_name='profile')
    # username, first_name, last_name, email, already defined in build in User Model
    # Add any additional attributes you want
    phone = models.CharField(max_length=40, null=True, blank=True) # add country prefix later
    congregation = models.ForeignKey(Congregation, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profiles')
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option=”build_ext” --global-option=”--disable-jpeg”
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    street = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=70, null=True, blank=True)
    country = models.CharField(max_length=70, null=True, blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username

    def get_absolute_url(self):
        return reverse('profiles:detail', kwargs={'pk':self.pk}) # For update and create views

    def get_picture(self):
        default_picture = settings.MEDIA_URL + 'profile_pics/default-picture.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pics/' + self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pics/' + self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                return default_picture
        except Exception:
            return default_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username
