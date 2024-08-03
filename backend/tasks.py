import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def send_verification_email(subject, message, recipient, html_message=None):
    logger.info(f"Sending email to {recipient}")
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, html_message=html_message)
    logger.info(f"Email sent to {recipient}")
