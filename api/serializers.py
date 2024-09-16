from dataclasses import field
from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    # (many=False) => cause we don't have multiple profiles(owners). we are gonna have just one.
    #  this owner field is gonna use 'ProfileSerializer' and can return a json object
    owner = ProfileSerializer(many=False)
    # (many=True) => cause we are gonna have multiple tags
    tags = TagSerializer(many=True)
    # we are gonna use 'SerializerMethodField' in here, because 'Review' model is a child to the 'Project' model
    # this attribute will be added to the 'Project' json object thanks to the below 'get_reviews' method field
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    # any field here has to start with 'get_'. so, has to start with that if we are gonna use 'SerializerMethodField'!
    # 'obj' is gonna be the object we are serializing, which would be the 'Project' model
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
    






