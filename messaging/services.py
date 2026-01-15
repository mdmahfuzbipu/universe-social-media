from django.db.models import Count

from .models import Message
from .models import Conversation


def get_or_create_conversation(user1, user2):
    conversation = (
        Conversation.objects.filter(participants=user1)
        .filter(participants=user2)
        .annotate(pcount=Count("participants"))
        .filter(pcount=2)
        .first()
    )

    if conversation:
        return conversation

    conversation = Conversation.objects.create()
    conversation.participants.add(user1, user2)
    return conversation


def send_message(conversation, sender, content):
    message = Message.objects.create(
        conversation=conversation, sender=sender, content=content
    )
    conversation.save()  
    return message
