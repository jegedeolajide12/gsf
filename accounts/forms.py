from logging import PlaceHolder
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from pages.views import units
from .models import CustomUser, Sermon, Profile

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


class SermonUploadForm(forms.ModelForm):
    class Meta:
        model = Sermon
        fields = [
            'sermon_file', 
            'preacher', 
            'date_preached', 
            'sermon_type', 
            'bible_reference', 
            'bible_text', 
            'title', 
            'description', 
            'sermon_series'
        ]
        widgets = {
            'sermon_file': forms.ClearableFileInput(attrs={'multiple': False, 'accept': '.mp3', 'class': 'file-input', 'required': True}),
            'date_preached': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True, 'placeholder': 'Select date', }),
            'bible_reference': forms.TextInput(attrs={'placeholder': 'e.g. John 3:16', 'class': 'form-control', 'required': True, 'placeholder': 'John 3:16'}),
            'preacher': forms.TextInput(attrs={'placeholder': 'Preacher Name', 'class': 'form-control', 'required': True, 'placeholder': 'Enter preacher\'s name'}),
            'sermon_type': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Select sermon type')] + list(Sermon.ServiceType.choices)),
            'bible_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter the Bible text here...', 'class': 'form-control', 'required': True, 'placeholder': 'For God so loved the world...'}),
            'title': forms.TextInput(attrs={'placeholder': 'Sermon Title', 'class': 'form-control', 'required': True, 'placeholder': 'Enter sermon title'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Sermon Description', 'class': 'form-control', 'required': True, 'placeholder': 'Enter a brief description of the sermon'}),
            'sermon_series': forms.TextInput(attrs={'placeholder': 'Sermon Series (if any)', 'class': 'form-control', 'required': False, 'placeholder': 'Enter sermon series if applicable'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['sermon_file'].required = True
        def clean_sermon_file(self):
            sermon_file = self.cleaned_data.get('sermon_file')
            if sermon_file:
                if not sermon_file.name.endswith('.mp3'):
                    raise forms.ValidationError("Only MP3 files are allowed.")
            return sermon_file

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


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'image', 'start_date', 'end_date', 'visibility', 'for_website', 'for_email', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter announcement title'}),
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': True, 'placeholder': 'Enter announcement content'}),
            'image': forms.ClearableFileInput(attrs={'multiple': False, 'class': 'announcement-file-input', 'required': False}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True, 'placeholder': 'Select start date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True, 'placeholder': 'Select end date'}),
            'visibility': forms.Select(attrs={'class': 'form-control', 'required': True},
                                       choices=Announcement.VisibilityChoices.choices),
            'for_website': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'for_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': True},
                                     choices=Announcement.CategoryChoices.choices),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")

        return cleaned_data
    
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