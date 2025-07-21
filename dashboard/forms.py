from django import forms

from .models import Sermon, Announcement, HomePageHero, DriveLink


class SermonCreationForm(forms.ModelForm):
    class Meta:
        model = Sermon
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sermon Title'}),
            'preached_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Choose Sermon Date'})
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'image', 'start_date', 'end_date', 'visibility', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter announcement title'}),
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': True, 'placeholder': 'Enter announcement content'}),
            'image': forms.ClearableFileInput(attrs={'type': 'file', 
                                                     'id': 'fileInput', 
                                                     'accept': 'image/*'
                                                     }),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True, 'placeholder': 'Select start date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True, 'placeholder': 'Select end date'}),
            'visibility': forms.Select(attrs={'class': 'form-control', 'required': True},
                                       choices=Announcement.VisibilityChoices.choices),
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



class HeroCreationForm(forms.ModelForm):
    class Meta:
        model = HomePageHero
        fields = ['title','image', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter hero title'}),
            'image': forms.ClearableFileInput(attrs={'multiple': False, 'id': 'fileInput', 'required': True}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': False, 'placeholder': 'Enter a brief description of the banner'}),
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
        fields = ['title', 'description', 'url', 'event', 'event_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter link title'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': False, 'placeholder': 'Enter a brief description of the link'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter the link URL'}),
            'event': forms.TextInput(attrs={'class': 'form-control', 'required': False, 'placeholder': 'Enter event name if applicable'}),
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': False, 'placeholder': 'Select event date'}),
        }
    
