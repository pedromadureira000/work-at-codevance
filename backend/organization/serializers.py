from rest_framework import serializers
from organization.models import SupplierCompany
from django.utils.translation import gettext_lazy as _

class SupplierCompanyPOSTSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(min_length=3, max_length=60)
    class Meta:
        model = SupplierCompany
        fields = ['company_name', 'cnpj']

#  class SupplierCompanyPUTSerializer(serializers.ModelSerializer):
    #  company_name = serializers.CharField(min_length=3, max_length=60)
    #  class Meta:
        #  model = SupplierCompany
        #  fields = ['company_name', 'cnpj']
        #  read_only_fields = ['contracting_code']


