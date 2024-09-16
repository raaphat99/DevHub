from multiprocessing import context
import profile
from turtle import title
from django.shortcuts import render, redirect
from django.http import HttpResponse

# this decorator is gonna set above any view that we want to block until a certain action is done(here until the user is logged in)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects
# Create your views here.


def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    
    # this attribute returns the index of the projects rendered on a certain page
    ''' print(projects.number) '''
    context = {'projects': projects, 'search_query': search_query,
                'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        # this just gonna give us the vote and the actual comment
        form = ReviewForm(request.POST)
        # getting the instance of the review
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        
        #Update project vote count
        projectObj.getVoteCount

        messages.success(request, 'Your review was successfully added!')
        return redirect('project', pk=projectObj.id)

    # accessing tags from this file (views.py), we can also access them from the template file
    # tags = projectObj.tags.all()
    context = {'project': projectObj, 'form': form}
    return render(request, 'projects/single-project.html', context)    


# the user have to log in to be able to create project, otherwise he is directed to the login page
@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newTags = request.POST.get('newtags').replace(',', " ").split()

        # when the user sumbits form static files(like images), we can get thsoe files in our back-end (static folder)
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # this gives us an instance of the current project
            project = form.save(commit=False)
            # assigns the newly created project to its creator
            project.owner = profile
            project.save()

            for tag in newTags:
                # this is gonna handle tags' duplicates (just in case)
                tag, created = Tag.objects.get_or_create(name=tag)
                # project has a field called 'tags', it is a many to many relationship.
                project.tags.add(tag)
                
            # when the submits the form, direct them to their account    
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    # this ensures that only the logged in user (the owner) can update his projects
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        # split method is gonna take each individual tag in the newTags list (they have to be separated by a space to be splitted correctly)
        newTags = request.POST.get('newtags').replace(',', " ").split()


        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newTags:
                # this is gonna handle tags' duplicates (just in case)
                tag, created = Tag.objects.get_or_create(name=tag)
                # project has a field called 'tags', it is a many to many relationship.
                project.tags.add(tag)

            return redirect('account')

    context = {'form': form, 'project': project}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    # this ensures that only the logged in user (the owner) can delete his proects
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)
