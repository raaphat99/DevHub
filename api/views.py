from urllib import request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# this is gonna be to return json data. (takes any python data we have and converts it into json data)
from rest_framework.response import Response 
from .serializers import ProjectSerializer
from projects.models import Project, Review, Tag

# this decorator is to make sure this is an api view, and it takes in a list of strings.
# we need to specify the type of the method (request) we can send
@api_view(['GET'])
def getRoutes(request):
    # Note: we need to serialize these pieces of data down here so, they can be converted into json objects
    # Serialization: is the process of converting our data form python objects form to json objects
    routes = [
        # this will return a list of project objects
        {'GET': '/api/projects'},
        # this will return the project associated with this id
        {'GET': '/api/projects/id'},
        # anytime someone clicks on a specific vote, we are sending them to this route and we are just saying that we wanna vote on this project
        {'POST': '/api/projects/id/vote'},
        
        # these two routes are gonna be to get a token (I could search about json web tokens until we get into them later)
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]

    return Response(routes) 

@api_view(['GET'])
# so any user wants to get projects here, they need to be authenticated
# this is similar to '@login_required' decorator we have used in users/views but, now this is for the django REST framework
# @permission_classes([IsAuthenticated])
def getProjects(request):
    # querying our projects, and then serialize them
    projects = Project.objects.all()
    # this serializer is gonna take this query set and turn it into json data
    serializer = ProjectSerializer(projects, many=True)
    # to get the data added to that serializer, we need to use the 'data' attribute
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    # querying our projects, and then serialize them
    project = Project.objects.get(id=pk)
    # this serializer is gonna take this query set and turn it into json data
    serializer = ProjectSerializer(project, many=False)
    # to get the data added to that serializer, we need to use the 'data' attribute
    return Response(serializer.data)

# we will allow the user to only send a POST request
@api_view(['POST'])
# this view will also require a user to be logged in (authenticated),
# that means that we need a valid token to make sure that the user can vote
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    # the project the user will vote on
    project = Project.objects.get(id=pk)
    # this user is coming from the token, not the session anymore, because of the above 'api_view' decorator
    # so, we are getting the user that is passed along in that token.
    user = request.user.profile
    # this is the body of the data that is sent over
    data = request.data
    # 'created' will be True if a new review is created or False if the user has already reviewed that project
    # 'review' will be the value of the vote (up/down)
    review, created = Review.objects.get_or_create(
        # the reviewer
        owner=user,
        project=project,
    )

    review.value = data['value']
    review.save()
    # update the totalVotes and the voteRatio
    project.getVoteCount

    # 'many=False' because we are getting a single instance of a project
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def removeTag(request):
    # get the data from the frontend to delete 
    tagId = request.data['tag']
    projectId = request.data['project']

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag)

    return Response('Tag was deleted!')

















