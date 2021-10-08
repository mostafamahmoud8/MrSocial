from django import forms
from .models import Group


class GroupForm(forms.ModelForm):
    image = forms.ImageField(required=False)
   
    class Meta:
        model = Group
        fields = ['name','description','image']

    def clean_name(self):
        name = self.cleaned_data['name']

        if name :
            return name
        else:
            raise forms.ValidationError('Name field is required')

