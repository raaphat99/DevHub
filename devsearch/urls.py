"""devsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
# importing settings, because we wanna have access to MEDIA-ROOT and MEDIA-URL
from django.conf import settings
# this helps us import static files
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # single quotes indicates the root's home page the user would be transferred to, once he accesses our website.
    # and we have used include function to link this urlpatterns list
    # to that one in projects app
    path('projects/', include('projects.urls')),
    path('', include('users.urls')),
    # we need to let this project know about our api
    # so, any route that starts with 'api', lets go ahead and include the 'api' folder 
    path('api/', include('api.urls')),

    # 1- User submits email for reset
    # this view is gonna render out a template and perform all the logic of sending out an email to the user
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
    # 2- Email sent message
    # this is gonna be that confirmation that the user gets to let him know that his email is sent 
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name="password_reset_done"),
    # 3- Email with link and reset instructions
    # the actual link that the user gets. this is where the user clicks on it, and then they can actually be taken to a form to reseet their password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"), name="password_reset_confirm"),
    # 4- Password successfully reset message
    # this is gonna be the final email that lets the user know that the password is reset, and they can now log in
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name="password_reset_complete"),
]



 # allow django to serve MEDIA-URL and STATIC-URL files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
