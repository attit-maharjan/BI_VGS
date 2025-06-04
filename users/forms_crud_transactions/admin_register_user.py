# users/forms_crud_transactions/admin_register_user.py

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

ROLE_CHOICES = [
    ("student", "Student"),
    ("teacher", "Teacher"),
    ("parent", "Parent"),
    ("admin", "Admin"),
]

GENDER_CHOICES = [
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
]

class AdminRegisterUserForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter password",
        })
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm password",
        })
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "gender",
            "dob",
            "profile_image",
        ]
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"})
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

    def clean_role(self):
        role = self.cleaned_data.get("role")
        if role not in ["student", "admin"]:
            raise ValidationError(
                "Currently, we only register Admin and Student roles. "
                "Please contact the Principal or Vice Principal for other roles."
            )
        return role

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

            # Automatically create associated profile based on role
            role = self.cleaned_data.get("role")
            if role == "student":
                from users.models import Student
                Student.objects.create(user=user)
            elif role == "teacher":
                from users.models import Teacher
                Teacher.objects.create(user=user)
            elif role == "parent":
                from users.models import Parent
                Parent.objects.create(user=user)

        return user
