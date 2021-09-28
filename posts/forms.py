from django import forms
from . import models

class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model  =  models.Post
        fields = ['content','image']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data['content']
        image   = cleaned_data['image']
    
        if not (image or content): 
            raise forms.ValidationError('you must add content or image to your post')
        else:
            return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model  =  models.Comment
        fields = ['message']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data['message']
    
        if not content: 
            raise forms.ValidationError('you must add content to your comment')
        else:
            return cleaned_data