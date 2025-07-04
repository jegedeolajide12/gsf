from django import forms
from .models import (
    Event, Semester, EventOccurence, UnitAnnouncement
    )


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