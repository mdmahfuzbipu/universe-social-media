from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "avatar",
            "cover_photo",
            "full_name",
            "bio",
            "date_of_birth",
            "location",
            "website",
            "education",
            "experience",
            "skills",
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "bio": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Tell something about yourself"}
            ),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "location": forms.TextInput(attrs={"placeholder": "Location"}),
            "website": forms.URLInput(attrs={"placeholder": "Website"}),
            "education": forms.TextInput(attrs={"placeholder": "Education"}),
            "experience": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Experience"}
            ),
            "skills": forms.TextInput(
                attrs={"placeholder": "Skills (comma separated)"}
            ),
        }
