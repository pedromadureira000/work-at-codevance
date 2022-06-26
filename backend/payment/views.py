from django.db import transaction
from django.db.models.query import Prefetch
from rest_framework import status
from rest_framework.response import Response
from organization.models import SupplierCompany
from payment.serializers import PaymentGETSerializer, PaymentHistorySerializer, PaymentPOSTSerializer, PaymentPUTSerializer, RequestAnticipationSerializer
from .models import Payment, PaymentHistory
from rest_framework.views import APIView
from settings.utils import has_permission, has_role
from drf_yasg.utils import swagger_auto_schema
from settings.response_templates import error_response, not_found_response, serializer_invalid_response, unauthorized_response, unknown_exception_response
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
import math
from datetime import datetime
import copy

class PaymentView(APIView):
    anticipation_status_query_string = openapi.Parameter('anticipation_status', openapi.IN_QUERY, description="1 => Available; 2 => Waiting confirmation; 3 => Anticipated; 4 => Unavailable; 5 => Denied", type=openapi.TYPE_STRING)

    response_schema_dict = {
        "200": openapi.Response(
            description="Payments",
            examples={
                "application/json": {
                    "id": 2,
                    "supplier_company": 2,
                    "operator": "operator",
                    "anticipation_status": 2,
                    "issuance_date": "2022-06-24T21:29:22.066000-03:00",
                    "due_date": "2022-06-24T21:29:22.066000-03:00",
                    "original_value": "13.00"
                }
            }
        ),
    }

    @swagger_auto_schema(method='get', responses=response_schema_dict, manual_parameters=[anticipation_status_query_string]) 
    @action(detail=False, methods=['get'])
    def get(self, request):
        if has_permission(request.user, 'get_payment'):
            kwargs = {}
            anticipation_status = request.GET.get("anticipation_status")
            if anticipation_status and anticipation_status in ["1", "2", "3", "4", "5"]: 
                kwargs.update({"anticipation_status": anticipation_status})
            if has_role(request.user, 'supplier_user'):
                payments = Payment.objects.filter(supplier_company_id=request.user.supplier_company_id, **kwargs)
                return Response(PaymentGETSerializer(payments, many=True).data)
            if has_role(request.user, 'operator'):
                payments = Payment.objects.filter(**kwargs)
                return Response(PaymentGETSerializer(payments, many=True).data)
            return unauthorized_response
        return unauthorized_response
    @swagger_auto_schema(request_body=PaymentPOSTSerializer) 
    @transaction.atomic
    def post(self, request):
        if has_role(request.user, 'operator'):
            serializer = PaymentPOSTSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as error:
                    transaction.rollback()
                    return unknown_exception_response(action=_('create payment'))
            return serializer_invalid_response(serializer.errors)
        return unauthorized_response 

class SpecificPaymentView(APIView):
    request_schema_dict = openapi.Schema(
        title=_("Update payment"),
        type=openapi.TYPE_OBJECT,
        properties={
            'anticipation_status': openapi.Schema(type=openapi.TYPE_STRING, description=_('Payment anticipation_status'), 
                example=1, enum=[1,2,3,4,5])
        }
    )

    @transaction.atomic
    @swagger_auto_schema(request_body=request_schema_dict, responses={200: 'Payment updated.'}) 
    def put(self, request, payment_id):
        if has_permission(request.user, 'update_payment'):
            try:
                payment = Payment.objects.get(id=payment_id)
            except Payment.DoesNotExist:
                return not_found_response(object_name=_('The payment'))
            serializer = PaymentPUTSerializer(payment, data=request.data, context={"request": request})
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(_('Payment updated.'))
                except Exception as error:
                    transaction.rollback()
                    #  print(error)
                    return unknown_exception_response(action=_('update payment'))
            return serializer_invalid_response(serializer.errors)
        return unauthorized_response

class RequestAnticipation(APIView):

    @transaction.atomic
    def post(self, request, payment_id):
        if has_permission(request.user, 'request_payment_anticipation'):
            if has_role(request.user, 'operator'):
                try:
                    payment = Payment.objects.get(id=payment_id)
                except Payment.DoesNotExist:
                    return not_found_response(object_name=_('The payment'))
            else:
                try:
                    payment = Payment.objects.get(id=payment_id, supplier_company_id=request.user.supplier_company_id)
                except Payment.DoesNotExist:
                    return not_found_response(object_name=_('The payment'))
            serializer = RequestAnticipationSerializer(payment, data=request.data, context={"request": request})
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Exception as error:
                    transaction.rollback()
                    #  print(error)
                    return unknown_exception_response(action=_('request anticipation'))
            return serializer_invalid_response(serializer.errors)
        return unauthorized_response 


class PaymentHistoryView(APIView):
    @transaction.atomic
    @swagger_auto_schema(method='get', responses={200: PaymentHistorySerializer(many=True)}) 
    @action(detail=False, methods=['get'])
    def get(self, request, payment_id):
        if has_permission(request.user, 'get_payment'):
            try:
                payment = Payment.objects.get(id=payment_id)
            except Payment.DoesNotExist:
                return not_found_response(object_name=_('The payment'))
            if has_role(request.user, 'supplier_user'):
                if payment.supplier_company_id != request.user.supplier_company_id:
                    return not_found_response(object_name=_('The payment'))
            try:
                payment_history = PaymentHistory.objects.filter(payment_id=payment_id).select_related('user')
            except PaymentHistory.DoesNotExist:
                return not_found_response(object_name=_('The payment history'))
            return Response(PaymentHistorySerializer(payment_history, many=True).data)
        return unauthorized_response
