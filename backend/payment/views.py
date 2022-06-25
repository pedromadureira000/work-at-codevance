from django.db import transaction
from django.db.models.query import Prefetch
from rest_framework import status
from rest_framework.response import Response
from organization.models import SupplierCompany
from payment.serializers import PaymentGETSerializer, PaymentHistorySerializer, PaymentPOSTSerializer, PaymentPUTSerializer
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


#  class fetchClientsToFillFilterSelectorToSearchOrders(APIView):
    #  @swagger_auto_schema(method='get', responses={200: ClientsToFillFilterSelectorsToSearchOrdersSerializer(many=True)})
    #  @action(detail=False, methods=['get'])
    #  def get(self, request):    
        #  if has_permission(request.user, 'get_orders') and not has_role(request.user, 'supplier_user'):
            #  if req_user_is_agent_without_all_estabs(request.user):
                #  clients = get_clients_with_client_users_by_agent(request.user)
                #  client_serializer = ClientsToFillFilterSelectorsToSearchOrdersSerializer(clients, many=True)
                #  return Response(client_serializer.data)
            #  clients = Client.objects.filter(client_table__contracting_id=request.user.contracting_id).prefetch_related('client_users')
            #  client_serializer = ClientsToFillFilterSelectorsToSearchOrdersSerializer(clients, many=True)
            #  return Response(client_serializer.data)
        #  return unauthorized_response


class PaymentView(APIView):
    anticipation_status_query_string = openapi.Parameter('anticipation_status', openapi.IN_QUERY, description="1 => Available; 2 => Waiting confirmation; 3 => Anticipated; 4 => Unavailable; 5 => Denied", type=openapi.TYPE_STRING)

    response_schema_dict = {
        "200": openapi.Response(
            description="Payments",
            examples={
                "application/json": {
                    #  "orders": [
                    #  "total": 1
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
                    return Response('ok', status=status.HTTP_201_CREATED)
                except Exception as error:
                    transaction.rollback()
                    return unknown_exception_response(action=_('create payment'))
            return serializer_invalid_response(serializer.errors)
        return unauthorized_response 

class SpecificPaymentView(APIView):
    #  @swagger_auto_schema(method='get', responses={200: PaymentDetailsSerializer}) 
    #  @action(detail=False, methods=['get'])
    #  def get(self, request, id):
        #  if has_permission(request.user, 'get_payment'):
            #  try:
                #  ordered_items = OrderedItem.objects.filter(order_id=id).select_related('item')
                #  order = Payment.objects.select_related('establishment', 'company', 'client', 'supplier_user', 
                        #  'price_table').prefetch_related(Prefetch('ordered_items', queryset=ordered_items
                            #  )).get(id=id, company__contracting_id=request.user.contracting_id)
            #  except Payment.DoesNotExist:
                #  return not_found_response(object_name=_('The order'))
            #  if has_role(request.user, 'supplier_user'):
                #  if order.client_id != request.user.client_id or order.client_user_id != request.user.user_code:
                    #  return not_found_response(object_name=_('The order'))
            #  if req_user_is_agent_without_all_estabs(request.user):
                #  if not request.user.establishments.filter(establishment_compound_id=order.establishment_id).first():
                    #  return not_found_response(object_name=_('The order'))
            #  return Response(PaymentDetailsSerializer(order).data)
        #  return unauthorized_response

    request_schema_dict = openapi.Schema(
        title=_("Update payment"),
        type=openapi.TYPE_OBJECT,
        properties={
            #  'ordered_items': openapi.Schema(type=openapi.TYPE_ARRAY, description=_('Ordered items list'), 
                #  items=openapi.Schema(type=openapi.TYPE_OBJECT, description=_('Ordered item'),
                    #  properties={
                        #  'item': openapi.Schema(type=openapi.TYPE_STRING, description=_('Item id'), example="123*123*0001"),
                        #  'quantity': openapi.Schema(type=openapi.TYPE_NUMBER, description=_('Ordered quantity'), example=12.33),
                        #  'sequence_number': openapi.Schema(type=openapi.TYPE_INTEGER, description=_('Sequence n the payment.'), 
                            #  example=1),
                        #  }
                #  )
            #  ),
            #  'anticipation_status': openapi.Schema(type=openapi.TYPE_STRING, description=_('Payment anticipation_status'), example=1, enum=[0,1,2,3,4,5]),
            #  'invoicing_date': openapi.Schema(type=openapi.TYPE_STRING, description=_('Invoice date'), example="2022-05-27T12:48:07.256Z", 
                #  format="YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]"),
            #  'invoice_number': openapi.Schema(type=openapi.TYPE_STRING, description=_('Invoice number'), example="123456789"),
            #  'note': openapi.Schema(type=openapi.TYPE_STRING, description=_('Client user note'), example=_("Client user note")),
            #  'agent_note': openapi.Schema(type=openapi.TYPE_STRING, description=_('Agent note'), example=_("Agent note")),
        }
    )

    @transaction.atomic
    @swagger_auto_schema(request_body=PaymentPUTSerializer, responses={200: 'Payment updated.'}) 
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

    response_schema_dict = {
        "200": openapi.Response(
            description="Payments",
            examples={
                "application/json": {
                    #  "orders": [
                    #  "total": 1
                }
            }
        ),
    }

    @transaction.atomic
    def post(self, request, payment_id):
        if has_permission(request.user, 'request_payment_anticipation'):
            try:
                payment = Payment.objects.get(id=payment_id, supplier_company_id=request.user.supplier_company_id)
            except Payment.DoesNotExist:
                return not_found_response(object_name=_('The payment'))
            if payment.anticipation_status != 1:
                return error_response(detail=_("You cannot request anticipation for this payment."), status=status.HTTP_400_BAD_REQUEST)
            try:
                # This is for accessing instance fields in the signals # TODO I should find a better way to do this.
                payment._old_instance = copy.copy(payment)
                payment._request_user = request.user
                payment.anticipation_status = 2
                payment.save()
                return Response('ok', status=status.HTTP_200_OK)
            except Exception as error:
                transaction.rollback()
                return unknown_exception_response(action=_('create payment'))
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
