from django.core.management import BaseCommand
from rolepermissions.roles import assign_role
from organization.models import SupplierCompany
from user.models import  User


class Command(BaseCommand):
    def handle(self, *args, **options):
        operator = User.objects.create_user(
            username="operator",
            email="operator@operator.phsw",
            password='asdf1234'
        )
        assign_role(operator, 'operator')

        supplier_company = SupplierCompany(company_name="SupComp", cnpj="26.827.665/0001-67")
        supplier_company.save()

        supplier_user = User.objects.create_user(
            username="supplier_user",
            email="supplier_user@supplier_user.phsw",
            password='asdf1234',
            supplier_company=supplier_company
        )
        assign_role(supplier_user, 'supplier_user')

        supplier_company2 = SupplierCompany(company_name="SupComp2", cnpj="49.337.628/0001-76")
        supplier_company2.save()

        supplier_user2 = User.objects.create_user(
            username="supplier_user2",
            email="supplier_user2@supplier_user2.phsw",
            password='asdf1234',
            supplier_company=supplier_company2
        )
        assign_role(supplier_user2, 'supplier_user')
