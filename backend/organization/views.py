from django.db.models.deletion import ProtectedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from organization.serializers import SupplierCompanyPOSTSerializer
from organization.models import SupplierCompany
from settings.utils import has_permission, has_role
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext_lazy as _
from settings.response_templates import error_response, not_found_response, serializer_invalid_response, protected_error_response, unknown_exception_response, unauthorized_response
from rest_framework.decorators import action

#  class ContractingView(APIView):
    #  @swagger_auto_schema(method='get', responses={200: ContractingPOSTSerializer(many=True)})
    #  @action(detail=False, methods=['get'])
    #  def get(self, request):
        #  if has_permission(request.user, 'get_contracting'):
            #  contractings = Contracting.objects.all()
            #  data = ContractingPOSTSerializer(contractings, many=True).data
            #  return Response(data)
        #  return unauthorized_response
    #  @swagger_auto_schema(request_body=ContractingPOSTSerializer) 
    #  @transaction.atomic
    #  def post(self, request):
            #  if has_permission(request.user, 'create_contracting'):
                #  data = request.data
                #  serializer = ContractingPOSTSerializer(data=data)
                #  if serializer.is_valid():
                    #  try:
                        #  serializer.save()
                        #  return Response(serializer.data)
                    #  except Exception as error:
                        #  transaction.rollback()
                        #  return unknown_exception_response(action=_("create contracting"))
                #  return serializer_invalid_response(serializer.errors)
            #  return unauthorized_response

#  class SpecificContracting(APIView):
    #  @swagger_auto_schema(request_body=ContractingPUTSerializer) 
    #  @transaction.atomic
    #  def put(self, request, contracting_code):
        #  if has_permission(request.user, 'update_contracting'):
            #  try:
                #  contracting = Contracting.objects.get(contracting_code=contracting_code)
            #  except Contracting.DoesNotExist:
                #  return Response({"error":[_( "The contracting company was not found.")]}, status=status.HTTP_404_NOT_FOUND)
            #  serializer = ContractingPUTSerializer(contracting, data=request.data, partial=True)
            #  if serializer.is_valid():
                #  try:
                    #  serializer.save()
                    #  return Response(serializer.data)
                #  except Exception as error:
                    #  transaction.rollback()
                    #  return unknown_exception_response(action=_('update contracting'))
            #  return serializer_invalid_response(serializer.errors)
        #  return unauthorized_response
    #  @transaction.atomic
    #  def delete(self, request, contracting_code):
        #  if has_permission(request.user, 'delete_contracting'):
            #  try:
                #  contracting = Contracting.objects.get(contracting_code=contracting_code)
            #  except Contracting.DoesNotExist:
                #  return Response({"error":[_( "The contracting company was not found.")]}, status=status.HTTP_404_NOT_FOUND)
            #  try:
                #  contracting.delete()
                #  return Response(_("Contracting deleted."))
            #  except ProtectedError:
                #  return Response({"error":[_("You cannot delete this contracting company because it has records linked to it.")]}, 
                        #  status=status.HTTP_400_BAD_REQUEST) 
            #  except Exception as error:
                #  transaction.rollback()
                #  return unknown_exception_response(action=_('delete contracting'))
        #  return unauthorized_response

