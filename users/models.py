import profile
from unittest import defaultTestLoader
from django.db import models
# a django built-in User model
from django.contrib.auth.models import User
import uuid

# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['created']

    # this property overcome breaking our website if a profile does not have a profile_image
    @property
    def imageURL(self):
        # if the image does exist, assign its url to this 'url' variable
        try:
            url = self.profile_image.url
        # if it doesn't, set the url to the default image
        except:
            url = ''
        return url


class Skill(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    # related_name attribute helps not to interfere this field with the 'sender' one
    # if we don't have it, we will not be allowed to have a connection with 'Profile' model twice
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    # Note:'blank' attribute default's value is False
    body = models.TextField()
    # if the message has been sent, it is obviously has not been read
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return self.subject
    
    # when the user opens his inpox, he should see the unread messages first
    # if there are not unread messages, the newer created messages will be at the top
    class Meta:
        ordering = ['is_read', '-created']



 