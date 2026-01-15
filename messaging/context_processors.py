from django.db.models import Q
from .models import Message, Conversation


def messaging_context(request):
    if not request.user.is_authenticated:
        return {}

    # Unread messages count (exclude messages sent by current user)
    unread_count = (
        Message.objects.filter(conversation__participants=request.user, is_read=False)
        .exclude(sender=request.user)
        .count()
    )

    # Get all conversations of this user, ordered by last updated
    conversations = (
        Conversation.objects.filter(participants=request.user)
        .order_by("-updated_at")
        .prefetch_related("participants", "messages")
    )

    # For each conversation, get the latest message not sent by the current user
    recent_messages = []
    for convo in conversations:
        last_msg = (
            convo.messages.exclude(sender=request.user).order_by("-created_at").first()
        )
        if last_msg:
            recent_messages.append(last_msg)

    # Limit to 5 latest conversations
    recent_messages = recent_messages[:5]

    return {
        "unread_messages_count": unread_count,
        "recent_messages": recent_messages,
    }
