from logging import PlaceHolder
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from pages.views import units
from .models import CustomUser, Profile

from allauth.account.forms import SignupForm

from pages.models import (
    HomePageBanner, HomePageHero, Announcement, DriveLink
)

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username',)


class CustomSignupForm(SignupForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email', 'class': 'form-control'}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'form-control'}),
        label='Password',
        help_text='Enter a strong password.',
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}),
        label='Confirm Password',
        help_text='Re-enter your password for confirmation.',
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'class': 'form-control'}),
        )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'class': 'form-control'}),
        )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number', 'class': 'form-control'}),
        )
    address = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Lodge Address', 'class': 'form-control'}),
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force widget for password1
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Enter Password', 'class': 'form-control'}
        )

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.address = self.cleaned_data.get('address', '')
        user.save()

        Profile.objects.create(
            user=user,
            phone_number=self.cleaned_data.get('phone', ''),
            address=self.cleaned_data.get('address', ''),
        )
        return user



class BannerCreationForm(forms.ModelForm):
    class Meta:
        model = HomePageBanner
        fields = ['image', 'title', 'description', 'event', 'action', 'start_date', 'end_date', 'mobile_image', 'visibility']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': False, 'class': 'file-input', 'required': True}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter banner title'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': False, 'placeholder': 'Enter a brief description of the banner'}),
            'event': forms.TextInput(attrs={'class': 'form-control', 'required': False, 'placeholder': 'Enter event name if applicable'}),
            'action': forms.Select(attrs={'class': 'form-control', 'required': True},
                                   choices=HomePageBanner.ActionChoices.choices),
            'action_url': forms.URLInput(attrs={'class': 'form-control', 'required': False, 'placeholder': 'Enter URL for action'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': False, 'placeholder': 'Select start date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': False, 'placeholder': 'Select end date'}),
            'mobile_image': forms.ClearableFileInput(attrs={'multiple': False, 'class': 'file-input', 'required': False, 'placeholder': 'Upload mobile image (optional)'}),
            'visibility': forms.Select(attrs={'class': 'form-control', 'required': True},
                                       choices=HomePageBanner.VisibilityChoices.choices),
            }
        def clean_image(self):
            image = self.cleaned_data.get('image')
            if image:
                if not image.name.endswith(('.png', '.jpg', '.jpeg')):
                    raise forms.ValidationError("Only PNG, JPG, and JPEG files are allowed.")
            return image

class HeroCreationForm(forms.ModelForm):
    class Meta:
        model = HomePageHero
        fields = ['title','image', 'description', 'event', 'mobile_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter hero title'}),
            'image': forms.ClearableFileInput(attrs={'multiple': False, 'class': 'file-input', 'required': True}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': False, 'placeholder': 'Enter a brief description of the banner'}),
            'event': forms.TextInput(attrs={'class': 'form-control', 'required': False, 'placeholder': 'Enter event name if applicable'}),
            'mobile_image': forms.ClearableFileInput(attrs={'multiple': False, 'class': 'file-input', 'required': False, 'placeholder': 'Upload mobile image (optional)'}),
            }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.name.endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("Only PNG, JPG, and JPEG files are allowed.")
        return image



class DriveLinkForm(forms.ModelForm):
    class Meta:
        model = DriveLink
        fields = ['title', 'description', 'url', 'event', 'visibility', 'event_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter link title'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': False, 'placeholder': 'Enter a brief description of the link'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter the link URL'}),
            'event': forms.TextInput(attrs={'class': 'form-control', 'required': False, 'placeholder': 'Enter event name if applicable'}),
            'visibility': forms.Select(attrs={'class': 'form-control', 'required': True},
                                       choices=DriveLink.VisibilityChoices.choices),
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': False, 'placeholder': 'Select event date'}),
        }
    

class WorkerUnitsForm():
    pass