from asyncio.windows_events import NULL
from multiprocessing import context
from pickle import GET
import profile
from unittest import installHandler
from django.forms import PasswordInput
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
# this decorator is gonna set any view that we want to block
from django.contrib.auth.decorators import login_required
# Flash Messages
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.models import User
# this is a utility that helps us extend our search
from django.db.models import Q
from .models import Profile, Message
from .utils import searchProfiles, paginateProfiles
# Create your views here.


def loginUser(request):

    page = 'login'

    # this if block restrict the user from accessing the login page if he has already been looged
    # user -> is the logged in user or an anonymous one
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            # we wanna make sure that the user is even exist in the data base
            user = User.objects.get(username=username)
        except:
            # if the user doesn't exist
            messages.error(request, 'Username does not exist!')

        # authenticate method takes in the username and the password and makes sure that they match
        # it returns either the user instance or NONE
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login function creates a session for the logged user, in the data base
            login(request, user)
    
            # if next is inside this request.GET method, send the user to its next value
            #  if it is a new user, then send him to his profile page
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or password is incorrect!')

    return render(request, 'users/login_register.html')


def logoutUser(request):

    # logout method takes in the request and deletes the session id
    logout(request)
    messages.info(request, 'User was successfully logged out.')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # instead of saving the form rightaway, we are saving it but we are holding a temporary instance of it.
            # this will create a user but we are holding it before we are processing it
            user = form.save(commit=False)
            # makes usernames lowercased before saving into the data base so, that way there is no case sensitivity 
            user.username = user.username.lower()
            user.save()
            # a flash message
            messages.success(request, 'User Created Successfully!')
            # let the user log in :)
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(
                request, 'An error has occurred during registeration!')
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    ourProfiles, search_query = searchProfiles(request)

    custom_range, ourProfiles = paginateProfiles(request, ourProfiles, 3)

    context = {'profiles': ourProfiles, 'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    # if a skill doesn't have a description, exclude it. (filter it out).
    topSkills = profile.skill_set.exclude(description__exact="")
    # every skill have an empty string as a decription, go ahead and give it to us.
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile': profile, 'topSkills': topSkills,
               'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)

# if the user isn't logged in, he won't be able to access the userAccount page and will be directed to the login page


@login_required(login_url='login')
def userAccount(request):
    # we get the user profile and render it in the account template
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        # request.POST for processing the form date, and
        # request.FILES for processing the images
        # instance indicates the profile we are updating
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    # processing the form data being inputted
    if request.method == 'POST':
        # we pass in the posted data
        form = SkillForm(request.POST)
        # we check that it is valid
        if form.is_valid():
            # now we can access the object and update the owner of the newly created skill
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(
                request, 'A new skill has been added successfuly!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
# we need to get the skill by its id to edit it
def updateSkill(request, pk):
    profile = request.user.profile
    # we wanna get the skill that we are modifying
    skill = profile.skill_set.get(id=pk)
    # this parameter tells us about the skill we are editing
    # that's gonna be pre filled with the information
    form = SkillForm(instance=skill)
    # processing the form data being inputted
    if request.method == 'POST':
        # we pass in the posted data
        form = SkillForm(request.POST, instance=skill)
        # we check that it is valid
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill has been updated successfuly!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    # fetch the skill we are gonna delete
    skill = profile.skill_set.get(id=pk)
    # deleting the skill
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill has been deleted successfuly!')
        return redirect('account')
    # we refers to 'object' in 'delete_template.html' file
    context = {'object': skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url='login')
def inbox(request):
    # get the currently logged in user
    profile = request.user.profile
    # 'messages' here is the related_name to 'recipient' field in the 'Message' model
    # we did it this way instead of saying 'profile.message_set.all()'
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    # get my profile (as a recipient)
    profile = request.user.profile
    # getting a particular message based on its id
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    # this is the guy that we are creating and sending the message to
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    # we first have to check if we have a sender (in the DB)
    try:
        # if the sender does exist, we are trying to get it
        sender = request.user.profile
    except:
        # if it does not, sender would be equal to None
        # (This means that the user is not logged in)
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid:
            # we wanna do this to catch 'sender' and 'recipient'
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            # if the user is logged in, the name and email fields will not be shown to him
            # so, we have to send thier values manually
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message is successfully sent!')
            # the sender will be directed to the recipient profile after sending the message
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)














































