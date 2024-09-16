import profile
from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.userProfile, name='user-profile'),
    path('account/', views.userAccount, name= 'account'),
    
    path('edit-account/', views.editAccount, name='edit-account'),
    
    path('create-skill', views.createSkill, name='create-skill'),
    path('update-skill/<str:pk>', views.updateSkill, name='update-skill'),
    path('delete-skill/<str:pk>', views.deleteSkill, name='delete-skill'),
    
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>', views.viewMessage, name='message'),
    # for the actual created message, we want to know which account this message is being created for
    # so we wanna know where we are sending this.
    path('create-message/<str:pk>', views.createMessage, name='create-message'),

]
