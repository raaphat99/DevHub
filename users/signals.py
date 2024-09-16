# these methods is gonna be triggered anytime an instance of a model is saved or deleted (after they are saved or deleted)
import profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# the django built-in User model
from django.contrib.auth.models import User

from .models import Profile
from django.core.mail import send_mail
from django.conf import settings


# 1- sender is gonna be the model that actually trigger the below function
# 2- instance is the instance of the model being saved
# 3- created is a true or false value that tells us if a new user was added or he was simply saved again
# (True -> a new commer has been added, False -> an exsisting one has been saved)
# 4- the @ tag makes a decorator. this is a more organized way to call our signal
# @receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
     
    # the instance is created for the first time
    if created:
        profile = Profile.objects.create(user=instance, username=instance.username,
                                         email=instance.email, name=instance.first_name)
        
        subject = 'Welcome to DevSearch!'
        message = 'We are glad you are here!'
        send_mail (
            subject,
            message,
            # the sender's email that django is gonna use to send new users the greeting messages
            settings.EMAIL_HOST_USER,
            # the recipient email (any new user who has just created a new account)
            [profile.email],
            fail_silently=False
        )



def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    # this means that this isn't the first time this instance is created
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
    

 # anytime a new user is being created, we are gonna trigger 'createProfile' method and create a profile to the user.
post_save.connect(createProfile, sender=User)
# anytime a profile is updated, we are gonna trigger the 'updateUser' mehthod and update the 'User' associated to it
post_save.connect(updateUser, sender=Profile)

# anytime an instance of the Profile model is deleted, we are gonna trigger 'deleteUser' mehthod
post_delete.connect(deleteUser, sender=Profile)
