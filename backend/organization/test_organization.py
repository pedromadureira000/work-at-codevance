from django.urls import reverse
import pytest
from model_bakery import baker
from django_assertions import assert_json_equal
from rest_framework.test import APIClient

from organization.models import SupplierCompany
drf_client = APIClient()  

@pytest.fixture
def get_supplier_companies__without_credentials(client):
    return client.get(reverse('supplier_company'))

def test__get_supplier_companies__without_credentials(get_supplier_companies__without_credentials):
    assert get_supplier_companies__without_credentials.status_code == 403 # Error: Forbidden
    assert_json_equal(get_supplier_companies__without_credentials.content,
        {
          "detail": "Authentication credentials were not provided."
        }
    )

@pytest.fixture
def supplier_companies(db):
    # XXX The cnpj field is not supported by baker
    supplier_company = baker.make(SupplierCompany, cnpj="99.999.999/0001-66")
    supplier_company.save()
    supplier_company2 = baker.make(SupplierCompany, cnpj="99.999.999/0001-66")
    supplier_company2.save()
    return [supplier_company, supplier_company2]

@pytest.fixture
def get_supplier_companies(client_with_logged_operator_user, supplier_companies):
    return client_with_logged_operator_user.get(reverse('supplier_company'))

def test__get_supplier_companies(get_supplier_companies, supplier_companies):
    assert get_supplier_companies.status_code == 200
    assert_json_equal(get_supplier_companies.content,
        [
          {
            "id": supplier_companies[0].id,
            "company_name": supplier_companies[0].company_name,
            "cnpj": supplier_companies[0].cnpj
          },
          {
            "id": supplier_companies[1].id,
            "company_name": supplier_companies[1].company_name,
            "cnpj": supplier_companies[1].cnpj
          }
        ]
    )
