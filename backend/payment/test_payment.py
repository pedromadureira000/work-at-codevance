from django.urls import reverse
import pytest
from model_bakery import baker
from django_assertions import assert_json_equal, assert_iqual
from rest_framework.test import APIClient

from organization.models import SupplierCompany
from payment.models import Payment
drf_client = APIClient()  
from datetime import timezone, datetime, timedelta
from random import randint
import json


@pytest.fixture
def get_payments__without_credentials(client):
    return client.get(reverse("payment:get_or_post_payment"))

def test__get_payments__without_credentials(get_payments__without_credentials):
    assert get_payments__without_credentials.status_code == 403 # Error: Forbidden
    assert_json_equal(get_payments__without_credentials.content,
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
def payments(db):
    payments = baker.make(Payment, 3, supplier_company=baker.make(SupplierCompany, cnpj="99.999.999/0001-66"))
    return payments

@pytest.fixture
def get_payments(client_with_logged_operator_user, payments):
    return client_with_logged_operator_user.get(reverse("payment:get_or_post_payment"))

def test__get_payments(get_payments, payments):
    serialized_payments = list(map(lambda x: {
        "id": x.id,
        "supplier_company": x.supplier_company_id,
        "operator": x.operator_id,
        "anticipation_status": x.anticipation_status,
        "issuance_date": x.issuance_date.replace(tzinfo=timezone.utc).astimezone(tz=None).isoformat(),
        "anticipation_due_date": x.anticipation_due_date.replace(tzinfo=timezone.utc).astimezone(tz=None).isoformat() if \
                x.anticipation_due_date else None,
        "due_date": x.due_date.replace(tzinfo=timezone.utc).astimezone(tz=None).isoformat(),
        "original_value": x.original_value.to_eng_string(),
        "new_value": x.new_value.to_eng_string() if x.new_value else None
    }, payments))
    
    assert get_payments.status_code == 200
    assert_json_equal(get_payments.content,
        serialized_payments
    )

@pytest.fixture
def supplier_company(db):
    supplier_company = baker.make(SupplierCompany, cnpj="99.999.999/0001-66")
    return supplier_company

@pytest.fixture
def post_payment(client_with_logged_operator_user, supplier_company):
    return client_with_logged_operator_user.post(reverse("payment:get_or_post_payment"), {
        "supplier_company": supplier_company.id,
        "due_date": (datetime.now() + timedelta(days=randint(1, 100))).replace(tzinfo=timezone.utc).astimezone(tz=None).isoformat(),
        "original_value": randint(1, 1000)
    }, format='json')

def test__post_payment(post_payment, supplier_company, logged_operator_user):
    response_dict = json.loads(post_payment.content)
    assert post_payment.status_code == 201 # Created
    assert ("supplier_company" in response_dict) and (response_dict["supplier_company"] == supplier_company.id)
    assert ("anticipation_status" in response_dict) and (response_dict["anticipation_status"] == 1)
    assert ("operator" in response_dict) and (response_dict["operator"] == logged_operator_user.username)
    assert "original_value" in response_dict
    assert "due_date" in response_dict
    assert "issuance_date" in response_dict

@pytest.fixture
def payment(db, logged_supplier_user):
    payment = baker.make(Payment, anticipation_status=1, supplier_company=logged_supplier_user.supplier_company)
    return payment

@pytest.fixture
def request_payment_anticipation__operator(client_with_logged_operator_user, payment):
    #  return client_with_logged_operator_user.post(reverse("payment:request_anticipation", kwargs={"payment_id": str(payment.id)}), format='json')
    return client_with_logged_operator_user.post(reverse("payment:request_anticipation", args=[payment.id]), format='json')

def test__request_payment_anticipation__operator(request_payment_anticipation__operator, payment):
    request_payment_anticipation__operator
    assert request_payment_anticipation__operator.status_code == 200
    assert_json_equal(request_payment_anticipation__operator.content,
        {
            "id": payment.id,
            "supplier_company": payment.supplier_company_id,
            "operator": payment.operator_id,
            "anticipation_status": 2,
            "issuance_date": payment.issuance_date.replace(tzinfo=timezone.utc).astimezone(tz=None).isoformat(),
            "anticipation_due_date": payment.anticipation_due_date.replace(tzinfo=timezone.utc).astimezone(tz=None).isoformat() if \
                    payment.anticipation_due_date else None,
            "due_date": payment.due_date.replace(tzinfo=timezone.utc).astimezone(tz=None).isoformat(),
            "original_value": payment.original_value.to_eng_string(),
        }
    )

@pytest.fixture
def payment_waiting_confirmation(db, logged_supplier_user):
    more_days = timedelta(days=randint(1, 100))
    due_date = datetime.now() + more_days
    anticipation_due_date = due_date - timedelta(days=randint(1, more_days.days))
    payment = baker.make(Payment, anticipation_status=2, supplier_company=logged_supplier_user.supplier_company, due_date=due_date,
            anticipation_due_date=anticipation_due_date)
    return payment

@pytest.fixture
def put_payment__anticipate(client_with_logged_operator_user, payment_waiting_confirmation):
    return client_with_logged_operator_user.put(reverse("payment:update_payment", args=[payment_waiting_confirmation.id]), {
        "anticipation_status": 3,
    }, format='json')

def test__put_payment__anticipate(put_payment__anticipate):
    assert put_payment__anticipate.status_code == 200
    assert_iqual(put_payment__anticipate.content,
        b'"Payment updated."'
    )


