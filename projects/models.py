from email.policy import default
from pyexpat import model
from tkinter import CASCADE
from django.db import models
import uuid
from users.models import Profile
# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # Null's Default value is = False
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000,  null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # uuid is a special field to store universally unique identifiers.
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    # when we render the project instances, we show its title instead of wierd symbols
    def __str__(self):
        return self.title
    
    class Meta:
        # when we render the projects, they will be ordered by their rating
        # the dash sign indicates the descending order. (the top rated with the highest number of votes would be listed first)
        # when equality happens, they would be ordered by their title
        ordering = ['created']
    
    # this property overcome breaking our website if a project does not have a featured_image
    @property
    def imageURL(self):
        # if the image does exist, assign its url to this 'url' variable
        try:
            url = self.featured_image.url
        # if it doesn't, set the url to the default image
        except:
            url = ''
        return url

    
    @property
    def reviewers(self):
        # this gives us an entire list of ids of people that have reviewed a project (an instance)
        # flat converts the result into a true list
        queryset = self.review_set.all().values_list('owner_id', flat=True)
        return queryset
    @property
    def getVoteCount(self):
        # this brings us all instances of the Review model
        reviews = self.review_set.all()
        # Positive votes
        upVotes = reviews.filter(value='Up').count()
        totalVotes = reviews.count()
        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()
        


class Review(models.Model):
    VOTE_TYPE = (
        ('Up', 'Up Vote'),
        ('Down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=2000, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    class Meta:
        # a user can only leave one review per project
        # so we can never have more than review with the same owner on the same project in the database
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
