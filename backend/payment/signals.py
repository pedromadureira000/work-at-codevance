from decimal import ROUND_HALF_UP, Decimal
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from .models import Payment, PaymentHistory
from settings.utils import has_role

@receiver(pre_save, sender=Payment)
def payment_pre_save(sender, instance, **kwargs):
    old_instance = getattr(instance, '_old_instance', None)
    request_user = getattr(instance, '_request_user', None)

    if old_instance:
        pass  # XXX I could do something here.


@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, created=False, **kwargs):
    old_instance = getattr(instance, '_old_instance', None)
    request_user = getattr(instance, '_request_user', None)

    #  Payment Inclusion
    if created:
        payment_history = PaymentHistory(payment=instance, user_id=instance.operator_id, history_type="I")
        payment_history.history_description = "- " + _("Payment created")
        payment_history.save()
    #  Payment Status Alteration
    else:
        payment_history = PaymentHistory(payment=instance, history_type="A", user=request_user, history_description="")
        #  Change payment anticipation_status
        if old_instance.anticipation_status != instance.anticipation_status:
            old_status = instance.get_anticipation_status_verbose_name(old_instance.anticipation_status)
            new_status = instance.get_anticipation_status_verbose_name(instance.anticipation_status)
            payment_history.history_description = _("- Payment anticipation status changed from '{old_status}' to '{new_status}'.").format(old_status=old_status, new_status=new_status)

        if old_instance.anticipation_due_date != instance.anticipation_due_date:
            if request_user.supplier_company:
                payment_history.history_description += _("\n- The supplier user requested a due date anticipation. The date requested was '{anticipation_due_date}'.").format(anticipation_due_date=instance.anticipation_due_date)
            else:
                payment_history.history_description += _("\n- The operator requested a due date anticipation. The date requested was '{anticipation_due_date}'.").format(anticipation_due_date=instance.anticipation_due_date)

        if old_instance.due_date != instance.due_date:
            payment_history.history_description += _("\n- Due date anticipation accepted. The new value is '{due_date}'.").format(due_date=instance.due_date)

        payment_history.save()
