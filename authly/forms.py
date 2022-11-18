from django import forms
from authly.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Frist name'}),required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'palceholder':'Last name'}),required=True)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'palceholder':'Bio'}),required=True)
    url = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'palceholder':'URL'}),required=True)
    location = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'palceholder':'Address'}),required=True)


    class Meta:
        model = Profile
        fields = ['image','first_name','last_name','bio','url','location']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'prompt srch_explore'}), max_length=50,required=True)

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email', 'class':'prompt srch_explore'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password', 'class':'prompt srch_explore'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password', 'class':'prompt srch_explore'}))


    class Meta:
        model = User
        fields = ['username','email','password1','password1']



















