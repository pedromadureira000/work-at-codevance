from django.db import models
from django.utils.translation import gettext_lazy as _

class Payment(models.Model):
    status_choices = (
        (1, _('Available')),
        (2, _('Waiting confirmation')),
        (3, _('Anticipated')),
        (4, _('Unavailable')),
        (5, _('Denied')),
    )
    # PaymentHistory_set
    class Meta:
        default_permissions = []
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
    supplier_company = models.ForeignKey('organization.SupplierCompany', on_delete=models.PROTECT, verbose_name=_('supplier company'))
    operator = models.ForeignKey('user.User', on_delete=models.PROTECT, verbose_name=_('operator'))
    anticipation_status = models.IntegerField(choices=status_choices)
    issuance_date = models.DateTimeField(auto_now_add=True, verbose_name=_('issuance date'))
    anticipation_due_date = models.DateTimeField(null=True, blank=True ,verbose_name=_('pending anticipation due date'))
    due_date = models.DateTimeField(verbose_name=_('due date'))
    original_value = models.DecimalField(max_digits=11, decimal_places=2, verbose_name=_('original value'))
    new_value = models.DecimalField(null=True, blank=True,max_digits=11, decimal_places=2, verbose_name=_('new value'))

    def get_anticipation_status_verbose_name(self, anticipation_status):
        return [value[1] for value in Payment._meta.get_field("anticipation_status").choices if value[0] == anticipation_status][0]

class PaymentHistory(models.Model):
    class Meta:
        default_permissions = []
        verbose_name = _('payment history')
        verbose_name_plural = _('payment histories')

    type_choices = (
        ('I', _('Inclusion')),
        ('A', _('Alteration')),
    )
    payment = models.ForeignKey('Payment', on_delete=models.DO_NOTHING, verbose_name=_('payment'), related_name='payment_history')
    user = models.ForeignKey('user.User', null=True, on_delete=models.DO_NOTHING, verbose_name=_('user'))
    history_type = models.CharField(choices=type_choices, max_length=2,verbose_name=_('history type'))
    history_description = models.CharField(verbose_name=_('history description'),max_length=800)
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('date'))
