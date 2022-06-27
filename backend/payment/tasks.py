from celery import shared_task
from django.core.mail import send_mail
from settings import settings
from .models import Payment
from datetime import datetime, timedelta

@shared_task(bind=True)
def send_mail_func(self, user_email, mail_subject, message):
    to_email = user_email
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )
    return "Done"


@shared_task(bind=True)
def invalidate_overdue_payment_anticipation_status(self):
    yesterday = datetime.now() - timedelta(days=1)
    payments = Payment.objects.filter(due_date__year=yesterday.year, due_date__month=yesterday.month, due_date__day=yesterday.day)
    for payment in payments:
        payment.anticipation_status = 4
        #  payment._old_instance = copy.copy(payment) # XXX Signals don't work here. This is not needed
    Payment.objects.bulk_update(payments, ['anticipation_status'])
    return "Done."
