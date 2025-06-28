from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Sermon

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username',)

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