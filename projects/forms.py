from django.forms import ModelForm, widgets
from django import forms
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        # the model we are creating the form for
        model = Project
        # this is the django way which creates a field for each attribute of the model class
        fields = ['title', 'featured_image', 'description',
                  'demo_link', 'source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)                              
        # self.fields['title'].widget.attrs.update(
        #     {'class':'input', 'placeholder': 'Add Title'}
        #     )
        # self.fields['description'].widget.attrs.update(
        #     {'class':'input', 'placeholder': 'Add Something'}
        #     )
        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
    
        labels = {
            'value': 'Place Your Vote!',
            'body': 'Please, Add a Comment with your vote!'
        }
    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)                              
        
        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input'})
