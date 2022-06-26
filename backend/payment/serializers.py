from django.db.models.query import Prefetch
from rest_framework import serializers
from settings.utils import has_role
from organization.models import SupplierCompany
from user.models import User
from .models import Payment, PaymentHistory
from django.utils.translation import gettext_lazy as _
import copy
from datetime import datetime
from django.utils import timezone

class PaymentGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'supplier_company', 'operator', 'anticipation_status', 'issuance_date', 'anticipation_due_date', 
                'due_date', 'original_value', 'new_value']
        read_only_fields = fields

class PaymentPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'supplier_company', 'operator', 'anticipation_status', 'issuance_date', 'due_date', 'original_value']
        read_only_fields = ['id', 'issuance_date', 'anticipation_status', 'operator']

    def validate_due_date(self, value):
        fixed_date = value.replace(hour=23, minute=59, second=59, microsecond=999999)
        now = timezone.now()
        if fixed_date < now:
            raise serializers.ValidationError(_("You cannot choose a due date earlier than today."))
        return fixed_date

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data, anticipation_status=1, operator=self.context['request'].user)
        return payment

class PaymentPUTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'supplier_company', 'operator', 'anticipation_status', 'issuance_date', 'due_date', 'original_value']
        read_only_fields = ['id', 'supplier_company', 'operator', 'issuance_date', 'due_date', 'original_value']

    def validate_anticipation_status(self, value):  
        if self.instance.anticipation_status in [4,5]:
            raise serializers.ValidationError(_("You cannot update this payment anymore."))
        if self.instance.anticipation_status == value : 
            raise serializers.ValidationError(_("You must choose a status value other than the current value."))
        if value == 2: 
            raise serializers.ValidationError(_("You cannot change the status to 'Waiting confirmation'. Only the supplier user can do that."))
        if value == 1: 
            raise serializers.ValidationError(_("You cannot change the status to 'Available'."))
        if self.instance.anticipation_status != 2 and value == 3: 
            raise serializers.ValidationError(_("You can only change the anticipation status to 'Anticipated' if the current status is 'Waiting confirmation'."))
        if self.instance.anticipation_status != 1 and value == 4: 
            raise serializers.ValidationError(_("You cannot change the status to 'Unavailable'."))
        return value

    def update(self, instance, validated_data):
        # This is for accessing instance fields in the signals
        instance._old_instance = copy.copy(instance)
        instance._request_user = self.context['request'].user
        if instance.anticipation_status == 2 and validated_data['anticipation_status'] == 3:
            validated_data['due_date'] = instance.anticipation_due_date
            days_difference = (instance.due_date - instance.anticipation_due_date).days 
            original_value = float(instance.original_value)
            validated_data['new_value'] = original_value - (original_value * ( (0.03/30) * days_difference))
        return super().update(instance, validated_data)


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = ['payment', 'user', 'history_type', 'history_description', 'date']
        read_only_fields = fields


class RequestAnticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'anticipation_due_date', 'supplier_company', 'operator', 'anticipation_status', 'issuance_date', 'due_date', 'original_value']
        read_only_fields = ['id', 'supplier_company', 'operator', 'anticipation_status', 'issuance_date', 'due_date','original_value']

    def validate_anticipation_due_date(self, value):
        new_date = value.replace(hour=23, minute=59, second=59, microsecond=999999)
        current_due_date = self.instance.due_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        now = timezone.now()
        if new_date < now:
            raise serializers.ValidationError(_("You cannot choose a due date earlier than today."))
        if value > current_due_date:  
            raise serializers.ValidationError(_("You must choose a due date earlier than the current due date."))
        return new_date

    def validate(self, attrs):
        if self.instance.anticipation_status != 1:
            raise serializers.ValidationError(_("You cannot request anticipation for this payment because the status is not 'Available'."))
        return super().validate(attrs)

    def update(self, instance, validated_data):
        # This is for accessing instance fields in the signals
        instance._old_instance = copy.copy(instance)
        instance._request_user = self.context['request'].user
        validated_data['anticipation_status'] = 2
        return super().update(instance, validated_data)

