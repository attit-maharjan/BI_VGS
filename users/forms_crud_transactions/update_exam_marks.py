
# ✅ File: users/forms_crud_transactions/update_exam_marks.py

from django import forms
from django.forms import formset_factory
from exams.models import StudentMark


class StudentMarkForm(forms.ModelForm):
    class Meta:
        model = StudentMark
        fields = ['score']

    def clean_score(self):
        score = self.cleaned_data.get('score')

        # Ensure score is numeric and between 0–100
        if score is not None:
            if not isinstance(score, (int, float, complex)) and not hasattr(score, '__float__'):
                raise forms.ValidationError("Score must be a number.")
            if score < 0 or score > 100:
                raise forms.ValidationError("Score must be between 0 and 100.")
        return score



UpdateStudentMarksFormSet = formset_factory(
    StudentMarkForm,
    extra=0,
    can_delete=False
)
