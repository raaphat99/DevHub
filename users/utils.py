# this is a utility that helps us extend our search
from django.db.models import Q
from .models import Profile, Skill
# Under the hood, all methods of pagination use the Paginator class.
# It does all the heavy lifting of actually splitting a QuerySet into Page objects.
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# passing the whole profile instances, and the number of ones we want to show on each page
def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    # Give Paginator a list of objects, plus the number of items you’d like to have on each page,
    # and it gives you methods for accessing the items for each page
    paginator = Paginator(profiles, results)

    try:
        # show me only (results number) profiles on the (page number) page
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        # this attribute tells us exactly how many pages we have
        # if the user went to a page that doesn't exist, direct him to the last page we have
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    # returns the chosen profiles
    return custom_range, profiles


def searchProfiles(request):
    # if we don't have any data from the front end, we wanna make sure it's an empty string so it doesn't ruin our filter
    search_query = ''
    # we wanna extract the value that is gonna be sent in search_query
    if request.GET.get('search_query'):
        # fetches the value we get from the frontend search bar
        search_query = request.GET.get('search_query')

    # skills are child items, these are in another model.
    # we fetch them and make sure that the search query matches our data in the database
    ourSkills = Skill.objects.filter(name__icontains=search_query)

    ourProfiles = Profile.objects.distinct().filter(
        # search for a profile by its name
        # we have used 'icontains' to handle case sensitivity
        # Q is a utility that helps us extend our search. we can use & (and) , | (or)
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        # Does the profile have a skill that's listed in the search bar (query set)?
        Q(skill__in=ourSkills)
    )
    return ourProfiles, search_query
