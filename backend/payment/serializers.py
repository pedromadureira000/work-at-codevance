from django.db.models.query import Prefetch
from rest_framework import serializers
from settings.utils import has_role
from organization.models import SupplierCompany
from user.models import User
from .models import Payment, PaymentHistory
from django.utils.translation import gettext_lazy as _
import copy

class PaymentGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'supplier_company', 'operator', 'anticipation_status', 'issuance_date', 'due_date', 'original_value']
        read_only_fields = fields

class PaymentPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'supplier_company', 'operator', 'anticipation_status', 'issuance_date', 'due_date', 'original_value']
        read_only_fields = ['id', 'anticipation_status', 'operator']

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data, anticipation_status=1, operator=self.context['request'].user)
        return payment

class PaymentPUTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'supplier_company', 'operator', 'anticipation_status', 'issuance_date', 'due_date', 'original_value']
        read_only_fields = ['id', 'supplier_company', 'operator', 'issuance_date', 'due_date', 'original_value']

        (4, _('Unavailable')),
        (5, _('Denied')),

    def validate_anticipation_status(self, value):  
        if self.instance.anticipation_status == value : 
            raise serializers.ValidationError(_("You must choose a status value other than the current value."))
        #  if self.instance.anticipation_status == 4 and value != 4: # TODO Add some validations?
            #  raise serializers.ValidationError(_("You cannot change ...."))
        #  if self.instance.anticipation_status == 5 and value != 5: 
            #  raise serializers.ValidationError(_("You cannot choose this option as anticipation status."))
        return value

    def update(self, instance, validated_data):
        # This is for accessing instance fields in the signals
        instance._old_instance = copy.copy(instance)
        instance._request_user = self.context['request'].user
        return super().update(instance, validated_data)


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = ['payment', 'user', 'history_type', 'history_description', 'date']
        read_only_fields = fields
