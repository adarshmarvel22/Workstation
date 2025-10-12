from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegistrationForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """User profile edit form"""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'user_type', 'bio', 'title',
            'profile_image', 'location', 'website', 'linkedin', 'github',
            'skills', 'interests'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Full Stack Developer, Product Designer'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
            'skills': forms.CheckboxSelectMultiple(),
            'interests': forms.CheckboxSelectMultiple(),
        }


class ProjectForm(forms.ModelForm):
    """Project creation and edit form"""

    class Meta:
        model = Project
        fields = [
            'title', 'short_description', 'description', 'project_type',
            'stage', 'status', 'collaboration_needed', 'cover_image', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Give your project a catchy name...',
                'class': 'form-control'
            }),
            'short_description': forms.TextInput(attrs={
                'placeholder': 'Brief one-liner about your project',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Describe your project in detail...',
                'class': 'form-control'
            }),
            'tags': forms.CheckboxSelectMultiple(),
            'project_type': forms.Select(attrs={'class': 'form-control'}),
            'stage': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'collaboration_needed': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()
        self.fields['tags'].widget.attrs['class'] = 'checkbox-list'


class MessageForm(forms.ModelForm):
    """Message form"""

    class Meta:
        model = Message
        fields = ['subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject (optional)',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Type your message...',
                'class': 'form-control'
            }),
        }


class ThoughtForm(forms.ModelForm):
    """Quick thought/post form"""

    class Meta:
        model = Thought
        fields = ['content', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Share your thoughts...',
                'class': 'form-control'
            }),
            'tags': forms.CheckboxSelectMultiple(),
        }


class CommentForm(forms.ModelForm):
    """Comment form"""

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a comment...',
                'class': 'form-control'
            }),
        }


class JoinRequestForm(forms.ModelForm):
    """Join request form"""

    class Meta:
        model = JoinRequest
        fields = ['message', 'desired_role']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us why you want to join this project...',
                'class': 'form-control'
            }),
            'desired_role': forms.TextInput(attrs={
                'placeholder': 'e.g., Frontend Developer, Marketing Lead',
                'class': 'form-control'
            }),
        }


class ProjectUpdateForm(forms.ModelForm):
    """Project update form"""

    class Meta:
        model = ProjectUpdate
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Update title',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Share your progress...',
                'class': 'form-control'
            }),
        }
        