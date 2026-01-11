from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    NOTIF_FOLLOW = "follow"
    NOTIF_REACTION = "reaction"
    NOTIF_COMMENT = "comment"
    NOTIF_SHARE = "share"

    NOTIF_CHOICES = [
        (NOTIF_FOLLOW, "Follow"),
        (NOTIF_REACTION, "Reaction"),
        (NOTIF_COMMENT, "Comment"),
        (NOTIF_SHARE, "Share"),
    ]

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_notifications"
    )
    notif_type = models.CharField(max_length=20, choices=NOTIF_CHOICES)
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, blank=True, null=True
    )
    comment = models.ForeignKey(
        "interactions.Comment", on_delete=models.CASCADE, blank=True, null=True
    )
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "read"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.sender} → {self.recipient} ({self.notif_type})"

    def get_message(self):
        if self.notif_type == self.NOTIF_FOLLOW:
            return "followed you."
        if self.notif_type == self.NOTIF_REACTION:
            return "reacted to your post."
        if self.notif_type == self.NOTIF_COMMENT:
            return "commented on your post."
        if self.notif_type == self.NOTIF_SHARE:
            return "shared your post."
        return ""


    def get_target_url(self):
        if self.notif_type == self.NOTIF_FOLLOW:
            return reverse("accounts:profile_detail", args=[self.sender.username])

        if self.post:
            return reverse("posts:feed") + f"#post-{self.post.id}"

        return "#"
