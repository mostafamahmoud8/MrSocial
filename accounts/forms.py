from django import forms
from django.core import  validators
from django.contrib.auth.forms import UserCreationForm ,UserChangeForm 
from django import forms
from .models import CustomUser
import datetime
import re
from django.utils.text import slugify


def validate_name(value):
    pattern = r'[A-Za-z]'
    if re.match(pattern,value):
        return value
    else:
        raise forms.ValidationError('this filed must contain only Character')

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(validators=[validators.EmailValidator('Enter a Valid Email address')])
    first_name = forms.CharField(max_length=150,required=True,validators=[validate_name])
    last_name = forms.CharField(max_length=150,required=True,validators=[validate_name])
    birth_date = forms.DateField(required=True)

    class Meta:
        model  = CustomUser
        fields = ['email','username','password1','password2','first_name','last_name','birth_date']
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date < datetime.date.today():
            return birth_date
        else:
            self.add_error('birth_date',forms.ValidationError('Please enter a valid birth date'))
    

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(validators=[validators.EmailValidator('Enter a Valid Email address')])
    first_name = forms.CharField(max_length=150,required=True,validators=[validate_name])
    last_name = forms.CharField(max_length=150,required=True,validators=[validate_name])
    birth_date = forms.DateField(required=True)
    image = forms.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ['email','username','first_name','last_name','birth_date','image']

