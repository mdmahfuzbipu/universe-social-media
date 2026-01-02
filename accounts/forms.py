from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Profile

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# Maximum file size: 10 MB
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

# Allowed image types
ALLOWED_TYPES = [
    "image/jpeg",  # .jpeg, .jpg
    "image/png",  # .png
    "image/gif",  # .gif
    "image/bmp",  # .bmp
    "image/webp",  # .webp
]


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
            "avatar": forms.FileInput(attrs={"class": "hidden"}),
            "cover_photo": forms.FileInput(attrs={"class": "hidden"}),
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


    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            # Check file size only for uploaded files
            if hasattr(avatar, "size") and avatar.size > MAX_UPLOAD_SIZE:
                raise ValidationError("Avatar file size should not exceed 10 MB.")

            # Check content type only for uploaded files
            if hasattr(avatar, "content_type") and avatar.content_type not in ALLOWED_TYPES:
                raise ValidationError(
                    "Only image files (JPEG, PNG, GIF, BMP, WEBP) are allowed for avatar."
                )
        return avatar


    def clean_cover_photo(self):
        cover = self.cleaned_data.get("cover_photo")
        if cover:
            if hasattr(cover, "size") and cover.size > MAX_UPLOAD_SIZE:
                raise ValidationError("Cover photo file size should not exceed 10 MB.")
            if hasattr(cover, "content_type") and cover.content_type not in ALLOWED_TYPES:
                raise ValidationError(
                    "Only image files (JPEG, PNG, GIF, BMP, WEBP) are allowed for cover photo."
                )
        return cover
