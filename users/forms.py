from pyexpat import model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message

# <UserCreationForm> is a django model form based on our User and is designed to add a user to the data base
# our right below class inherts all functionalities existed in UserCreationForm model
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        # changes the first_name field's label
        labels = {
            'first_name': 'Name',
        }
    
    def __init__(self, *args, **kwargs):
        # inherits from CustomUserCreationForms so we wanna let it know what are the fields it will be working with
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)                              
    
        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input'})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'bio',
                    'short_intro', 'profile_image', 'social_github',
                    'social_linkedin', 'social_twitter',
                    'social_website']
    
    def __init__(self, *args, **kwargs):
        # inherits from ProfileForm so we wanna let it know what are the fields it will be working with
        super(ProfileForm, self).__init__(*args, **kwargs)                              
        # applying some styling into our form with the help of 'class': 'input' rule set
        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input'})

    
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        # all fields of Skill model will be generated in this form except the 'owner' field
        exclude = ['owner']
    
    def __init__(self, *args, **kwargs):
        # inherits from SkillForm so we wanna let it know what are the fields it will be working with
        super(SkillForm, self).__init__(*args, **kwargs)                              
        # applying some styling into our form with the help of 'class': 'input' rule set
        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
            # inherits from MessageForm so we wanna let it know what are the fields it will be working with
            super(MessageForm, self).__init__(*args, **kwargs)                              
            # applying some styling into our form fields with the help of 'class': 'input' rule set
            for key, value in self.fields.items():
                value.widget.attrs.update({'class': 'input'})








