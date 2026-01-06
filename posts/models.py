from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    content = models.TextField(blank=True)  
    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)

    original_post = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="shares"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["original_post"]),  
        ]

    def __str__(self):
        return f"Post by {self.author}"