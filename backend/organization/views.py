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

class SupplierCompanyView(APIView):
    @swagger_auto_schema(method='get', responses={200: SupplierCompanyPOSTSerializer(many=True)})
    @action(detail=False, methods=['get'])
    def get(self, request):
        if has_permission(request.user, 'get_supplier'):
            supplier_companies = SupplierCompany.objects.all()
            data = SupplierCompanyPOSTSerializer(supplier_companies, many=True).data
            return Response(data)
        elif has_role(request.user, 'supplier_user'): # If it is the supplier user
            supplier_companies = SupplierCompany.objects.filter(id=request.user.supplier_company_id)
            data = SupplierCompanyPOSTSerializer(supplier_companies, many=True).data
            return Response(data)
        return unauthorized_response

