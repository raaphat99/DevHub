from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    # this view is gonna generate a token based on a user
    # (when we hit this endpoint and we submit our username and password, this is gonna generate json web token for us)
    TokenObtainPairView,
    # this is gonna generate something called a refreash token
    TokenRefreshView,
)
# Long Note about refreash tokens:
'''
 a token is gonna be stored in the browser somewhere, and it typically has a short life span like 5 minutes or so.
 so, just to make sure that this token doesn't get stolen by a hacker or something, this token expires.
 and we wanna do is securely store something called a refreash token.
 This refreash token will have a longer life span, and this can be 30 days or a year or however long we wanted.
'''
urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>/', views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote),

    path('remove-tag/', views.removeTag),
    
]