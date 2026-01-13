from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Count, Q, OuterRef, Subquery
from django.contrib import messages

from .models import Conversation, Message
from .services import send_message
from django.contrib.auth import get_user_model
from .services import get_or_create_conversation


# Create your views here.

User = get_user_model()

@login_required
def start_conversation(request, username):
    other_user = get_object_or_404(User, username=username)

    if other_user == request.user:
        return redirect("messaging:inbox")

    conversation = get_or_create_conversation(request.user, other_user)

    return redirect("messaging:detail", convo_id=conversation.id)


@login_required
def delete_conversation(request, convo_id):
    conversation = get_object_or_404(
        Conversation, id=convo_id, participants=request.user
    )

    # Soft delete for current user
    conversation.participants_deleted.add(request.user)

    messages.success(request, "Conversation deleted successfully.")
    return redirect("messaging:inbox")


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(participants=request.user).exclude(
        participants_deleted=request.user
    )

    last_message_qs = Message.objects.filter(
        conversation=OuterRef("pk"), is_deleted=False
    ).order_by("-created_at")

    conversations = conversations.annotate(
        last_message_text=Subquery(last_message_qs.values("content")[:1]),
        last_message_time=Subquery(last_message_qs.values("created_at")[:1]),
        last_message_sender_id=Subquery(last_message_qs.values("sender_id")[:1]),
        unread_count=Count(
            "messages",
            filter=Q(messages__is_read=False, messages__is_deleted=False)
            & ~Q(messages__sender=request.user),
        ),
    ).order_by("-last_message_time")

    # a dict mapping convo.id -> other_user
    other_users = {
        convo.id: convo.get_other_user(request.user) for convo in conversations
    }

    return render(
        request,
        "messaging/inbox.html",
        {
            "conversations": conversations,
            "other_users": other_users,
        },
    )


@login_required
def conversation_detail(request, convo_id):
    conversation = get_object_or_404(
        Conversation, id=convo_id, participants=request.user
    )

    if conversation.participants_deleted.filter(id=request.user.id).exists():
        messages.warning(request, "This conversation was deleted.")
        return redirect("messaging:inbox")

    chat_messages = conversation.messages.filter(is_deleted=False).order_by(
        "created_at"
    )

    Message.objects.filter(
        is_read=False, conversation=conversation, is_deleted=False
    ).exclude(sender=request.user).update(is_read=True, read_at=now())

    other_user = conversation.get_other_user(request.user)

    return render(
        request,
        "messaging/detail.html",
        {
            "conversation": conversation,
            "chat_messages": chat_messages,
            "other_user": other_user,
        },
    )


@login_required
def send_message_view(request, convo_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    conversation = get_object_or_404(
        Conversation, id=convo_id, participants=request.user
    )

    content = request.POST.get("content", "").strip()

    if not content:
        return JsonResponse({"error": "Message cannot be empty"}, status=400)

    message = send_message(conversation, request.user, content)

    return JsonResponse(
        {
            "id": message.id,
            "content": message.content,
            "sender_id": message.sender.id,
            "sender_username": message.sender.username,
            "sender_avatar": message.sender.profile.avatar.url,
            "created_at": message.created_at.strftime("%H:%M"),
        }
    )


@login_required
def mark_message_as_read(request, message_id):
    message = get_object_or_404(
        Message, id=message_id, conversation__participants=request.user
    )

    if not message.is_read:
        message.mark_as_read()

    return redirect(request.GET.get("next", message.get_absolute_url()))


@login_required
def mark_conversation_as_read(request, convo_id):
    conversation = get_object_or_404(
        Conversation, id=convo_id, participants=request.user
    )

    Message.objects.filter(
        conversation=conversation, is_read=False, is_deleted=False
    ).exclude(sender=request.user).update(is_read=True, read_at=now())

    return redirect("messaging:inbox")


