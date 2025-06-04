from django import forms
from the_school.models import SchoolSettings

class SchoolSettingsForm(forms.ModelForm):
    class Meta:
        model = SchoolSettings
        fields = '__all__'
        widgets = {
            'established_year': forms.NumberInput(attrs={'placeholder': 'e.g. 1990'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'homepage_intro': forms.Textarea(attrs={'rows': 2}),
            'privacy_policy': forms.Textarea(attrs={'rows': 3}),
            'terms_of_service': forms.Textarea(attrs={'rows': 3}),
            'about_us_paragraph1': forms.Textarea(attrs={'rows': 3}),
            'about_us_paragraph2': forms.Textarea(attrs={'rows': 3}),
            'about_us_paragraph3': forms.Textarea(attrs={'rows': 3}),
            'contact_us_paragraph1': forms.Textarea(attrs={'rows': 3}),
            'contact_us_paragraph2': forms.Textarea(attrs={'rows': 3}),
            'social_media_links': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '{"Facebook": "https://fb.com/school"}'
            }),
        }
