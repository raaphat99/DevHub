from django.db.models import Q
from .models import Project, Tag
# Under the hood, all methods of pagination use the Paginator class.
# It does all the heavy lifting of actually splitting a QuerySet into Page objects.
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# passing the whole project instances, and the number of ones we want to show on each page
def paginateProjects(request, projects, results):
    page = request.GET.get('page')
    
    # Give Paginator a list of objects, plus the number of items you’d like to have on each page,
    # and it gives you methods for accessing the items for each page
    paginator = Paginator(projects, results)

    try:
        # show me only (results number) projects on the (page number) page
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        # this attribute tells us exactly how many pages we have
        # if the user went to a page that doesn't exist, direct him to the last page we have
        page = paginator.num_pages
        projects = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    # returns the chosen projects
    return custom_range, projects


def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        # fetches the value we get from the frontend search bar
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )
    return projects, search_query