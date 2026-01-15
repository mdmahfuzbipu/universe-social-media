from django.conf import settings
from django.db import models
from django.utils.timezone import now

User = settings.AUTH_USER_MODEL


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    participants_deleted = models.ManyToManyField(
        User, related_name="deleted_conversations", blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-updated_at"]
    
    def __str__(self):
        return f"Conversation {self.id}"
    
    def get_other_user(self, user):
        return self.participants.exclude(id=user.id).first()


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # NOTE: Global delete for MVP. Will migrate to per-user delete later

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["conversation", "created_at"]),
            models.Index(fields=["is_read"]),
            models.Index(fields=["sender"]),
        ]

    def __str__(self):
        return f"Message {self.id} in {self.conversation}"  

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = now()
            self.save(update_fields=["is_read", "read_at"])

    def mark_as_deleted(self):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def get_absolute_url(self):
        return f"/messaging/conversations/{self.conversation.id}/"

    def snippet(self):
        return self.content[:30] + ("..." if len(self.content) > 30 else "")
