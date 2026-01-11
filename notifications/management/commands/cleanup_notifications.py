from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from notifications.models import Notification


class Command(BaseCommand):
    help = "Delete notifications older than 30 days"

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=30)
        deleted, _ = Notification.objects.filter(created_at__lt=cutoff).delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted} old notifications"))
