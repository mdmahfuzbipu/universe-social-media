from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
        indexes = [
            models.Index(fields=["follower", "following"]),
        ]

    def __str__(self):
        return f"{self.follower} → {self.following}"


class Reaction(models.Model):
    REACTION_LIKE = "like"
    REACTION_LOVE = "love"
    REACTION_HAHA = "haha"
    REACTION_WOW = "wow"
    REACTION_SAD = "sad"
    REACTION_DISLIKE = "dislike"

    REACTION_CHOICES = [
        (REACTION_LIKE, "Like"),
        (REACTION_LOVE, "Love"),
        (REACTION_HAHA, "Haha"),
        (REACTION_WOW, "Wow"),
        (REACTION_SAD, "Sad"),
        (REACTION_DISLIKE, "Dislike"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="reactions"
    )
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["post", "reaction"]),
        ]

    def __str__(self):
        return f"{self.user} reacted {self.reaction} on post {self.post_id}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["post", "created_at"]),
        ]

    def __str__(self):
        return f"Comment by {self.user} on post {self.post_id}"
