from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import (
    Event, Semester, EventOccurence, UnitAnnouncement, AcademicArticle, EducationalMaterial,
    MotivationalWriteup, Scholarship
    )

from django_summernote.widgets import SummernoteWidget
from taggit.forms import TagWidget


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True, 'placeholder': 'Select start date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True, 'placeholder': 'Select end date'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter semester name'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date cannot be after end date.")
        
        return cleaned_data

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'image', 'semester', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter event title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter event description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'file-input', 'required': False}),
            'semester': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter event location'}),
        }

class EventOccurrenceForm(forms.ModelForm):
    class Meta:
        model = EventOccurence
        fields = ['date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True, 'placeholder': 'Select date'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'required': True, 'placeholder': 'Select time'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Expecting 'event' to be passed in kwargs to link occurrence to the event being created
        event = kwargs.pop('event', None)
        if event is not None:
            self.instance.event = event

class UnitAnnouncementForm(forms.ModelForm):

    class Meta:
        model = UnitAnnouncement
        fields = ['title', 'content', 'image', 'start_date', 'end_date', 'visibility', 'for_website', 'for_email', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter announcement title'}),
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': True, 'placeholder': 'Enter announcement content'}),
            'image': forms.ClearableFileInput(attrs={'multiple': False, 'class': 'announcement-file-input', 'required': False}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True, 'placeholder': 'Select start date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True, 'placeholder': 'Select end date'}),
            'visibility': forms.Select(attrs={'class': 'form-control', 'required': True},
                                       choices=UnitAnnouncement.VisibilityChoices.choices),
            'for_website': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'for_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': True},
                                     choices=UnitAnnouncement.CategoryChoices.choices),
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


class AcademicArticleForm(forms.ModelForm):
    class Meta:
        model = AcademicArticle
        fields = ['title', 'thumbnail', 'content', 'tags', 'publication_date', 'visibility']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter article title'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'announcement-file-input', 'required': False, 'placeholder': 'Upload thumbnail image'}),
            'tags': TagWidget(attrs={'class': 'form-control', 'placeholder': 'Add tags (e.g., Book, God, Faith)'}),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
            'publication_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True, 'placeholder': 'Select publication date'}),
            'visibility': forms.Select(attrs={'class': 'form-control', 'required': True},
                                       choices=AcademicArticle.VisibilityChoices.choices),
        }

class EducationalMaterialForm(forms.ModelForm):
    class Meta:
        model = EducationalMaterial
        fields = ['title', 'course', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'e.g MTS101 Material...'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': True, 'placeholder': 'Enter Material content'}),
            'file': forms.ClearableFileInput(attrs={'multiple': False, 'class': 'announcement-file-input', 'required': False}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter the Course name.'})
        }


class MotivationalWriteupForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'quote', 'upload_date', 'visibility']
        model = MotivationalWriteup
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter Writeup Title'}),
            'quote': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': True, 'placeholder': 'Enter Material content'}),
            'upload_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True, 'placeholder': 'Select upload date'}),
            'visibility': forms.Select(attrs={'class': 'form-control', 'required': True})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        upload_date = cleaned_data.get('upload_date')

        if upload_date and upload_date < timezone.now():
            raise forms.ValidationError("The upload date cannot be in the past.")
        
        return cleaned_data

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['title', 'description', 'eligibility_criteria', 'deadline', 'amount', 'image', 'url', 'tags', 'visibility']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter scholarship title'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': True, 'placeholder': 'Enter scholarship description'}),
            'eligibility_criteria': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': True, 'placeholder': 'Enter eligibility criteria'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True, 'placeholder': 'Select application deadline'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter scholarship amount'}),
            'image': forms.ClearableFileInput(attrs={'class': 'announcement-file-input', 'required': False}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'required': False, 'placeholder': 'Enter scholarship URL (if any)'}),
            'tags': TagWidget(attrs={'class': 'form-control', 'placeholder': 'Add tags (e.g., Education, Scholarship, Funding)'}),
            'visibility': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        deadline = cleaned_data.get('deadline')

        if deadline and deadline < timezone.now():
            raise forms.ValidationError("The deadline cannot be in the past.")
        
        return cleaned_data