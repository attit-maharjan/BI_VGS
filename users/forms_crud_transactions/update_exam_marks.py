from django import forms
from exams.models import StudentMark

class StudentMarkForm(forms.ModelForm):
    class Meta:
        model = StudentMark
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={
                'min': 0,
                'max': 100,
                'step': '0.01',
                'class': 'form-input'
            })
        }

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score is None:
            raise forms.ValidationError("Score is required.")
        if not (0 <= score <= 100):
            raise forms.ValidationError("Score must be between 0 and 100.")
        return score
