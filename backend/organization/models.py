from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cpf_cnpj.fields import CNPJField

class SupplierCompany(models.Model):
    # User_set
    class Meta:
        default_permissions = []
        verbose_name = _('supplier company')
        verbose_name_plural = _('supplier companies')
    company_name = models.CharField(max_length=60, verbose_name=_("company name"))
    cnpj = CNPJField(masked=True, verbose_name="CNPJ")
    def __str__(self):
        return f'Contracting: {self.company_name}'
