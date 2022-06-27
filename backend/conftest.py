import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from rolepermissions.roles import assign_role

from organization.models import SupplierCompany

client = APIClient()

@pytest.fixture
def logged_operator_user(db, django_user_model):
    user = baker.make(django_user_model, username="test_operator_user", email="test@operator_user.anything")
    password = "safe_password_123"
    user.set_password(password)
    user.save()
    assign_role(user, 'operator')
    return user

@pytest.fixture
def client_with_logged_operator_user(logged_operator_user):
    client.force_login(logged_operator_user)
    return client

@pytest.fixture
def logged_supplier_user(db, django_user_model):
    supplier_company = SupplierCompany(company_name="SupComp", cnpj="99.999.999/0001-66")
    supplier_company.save()
    user = baker.make(django_user_model, username="test_supplier_user", email="test@supplier_user.anything")
    user.supplier_company = supplier_company
    password = "safe_password_123"
    user.set_password(password)
    user.save()
    assign_role(user, 'supplier_user')
    return user

@pytest.fixture
def client_with_logged_supplier_user(logged_supplier_user):
    client.force_login(logged_supplier_user)
    return client
