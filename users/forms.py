"""
users/forms.py

Purpose:
- Handle custom email-based login authentication
- Handle user profile updates (edit profile form)
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from PIL import Image


# =====================================================
# 🔐 USER MODEL
# =====================================================
User = get_user_model()


# =====================================================
# 📧 Email-Based Authentication Form
# =====================================================
class EmailAuthenticationForm(AuthenticationForm):
    """
    Login using email + password instead of username.
    Includes 'Remember Me' logic and active-user validation.
    """

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email",
            "autofocus": True,
        })
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password"
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        label="Remember Me",
        widget=forms.CheckboxInput()
    )

    def confirm_login_allowed(self, user):
        """
        Only allow active users to log in.
        """
        if not user.is_active:
            raise ValidationError("This account is inactive.", code='inactive')


# =====================================================
# 🛠 User Profile Update Form
# =====================================================
class UserUpdateForm(forms.ModelForm):
    """
    Form for editing user profile, including image validation.
    """

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'initials', 'dob', 'gender',
            'phone_number', 'profile_image',
            'street_address', 'city', 'state_province', 'postal_code', 'country'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_profile_image(self):
        """
        Validate uploaded profile image:
        - Size <= 5MB
        - Dimensions: 100x100 to 1500x1500 pixels
        """
        image = self.cleaned_data.get('profile_image')

        if image:
            max_size = 5 * 1024 * 1024  # 5MB
            if image.size > max_size:
                raise ValidationError("The image file size exceeds the 5MB limit.")

            img = Image.open(image)
            width, height = img.size

            if width < 100 or height < 100:
                raise ValidationError("Image must be at least 100x100 pixels.")
            if width > 1500 or height > 1500:
                raise ValidationError("Image cannot exceed 1500x1500 pixels.")

        return image
