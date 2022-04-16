from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Post


class EmailForm(forms.Form):
    email = forms.EmailField(required=True, label='', widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                                                     'class': 'form-control'}))


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False,
                              widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(required=False,
                          widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class NewPostForm(forms.ModelForm):
    title = forms.CharField(label="Название", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label="Текст", required=True, widget=forms.Textarea(attrs={'class': 'form-conrol'}))

    class Meta:
        model = Post
        fields = ['title', 'body']
