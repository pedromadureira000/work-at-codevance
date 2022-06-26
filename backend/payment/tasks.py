from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from payment.models import Payment
from settings import settings
from django.utils import timezone
from datetime import timedelta
import copy

@shared_task(bind=True)
def invalidate_anticipation_status(self, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        return "Payment not found. Something went wrong here."

    if payment.anticipation_status in [3,4,5]:
        return "Nothing to change."
    payment._old_instance = copy.copy(payment) # for the signal
    payment.anticipation_status = 4
    payment.save()
    return "Done."


@shared_task(bind=True)
def send_mail_func(self):
    users = get_user_model().objects.all()
    #  timezone.localtime(users.date_time) + timedelta(days=2)
    for user in users:
        mail_subject = "Hi! Celery Testing"
        message = "If you are liking my content, please hit the like button and do subscribe to my channel"
        to_email = user.email
        send_mail(
            subject = mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "Done"
