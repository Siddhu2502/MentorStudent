from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import logging

from .models import Evaluation

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Evaluation)
def send_email_on_submit(sender, instance, created, **kwargs):
    if not created and instance.is_submitted:
        subject = f"Evaluation Marks Submitted for {instance.student.name}"
        message = f"Dear {instance.student.name},\n\nYour marks have been submitted.\n\nThanks"
        from_email = None
        recipient_list = [instance.student.email]
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            logger.info(f"Email sent to {instance.student.email}")
        except Exception as e:
            logger.error(f"Failed to send email to {instance.student.email}: {str(e)}")