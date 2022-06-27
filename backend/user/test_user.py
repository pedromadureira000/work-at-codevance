from django.urls import reverse
import pytest
from model_bakery import baker
from django_assertions import assert_iqual, assert_json_equal
from rest_framework.test import APIClient

from organization.models import SupplierCompany
drf_client = APIClient()  
from rolepermissions.roles import assign_role


@pytest.fixture
def operator_user(django_user_model):
    user = baker.make(django_user_model)
    password = "ThisPassword123@"
    user.set_password(password)
    user.save()
    assign_role(user, 'operator')
    user.plain_text_password = password
    return user

@pytest.fixture
def supplier_user(django_user_model):
    user = baker.make(django_user_model)
    supplier_company = SupplierCompany(company_name="SomeComp", cnpj="99.999.999/0001-66")
    supplier_company.save()
    user.supplier_company = supplier_company
    password = "ThisPassword123@"
    user.set_password(password)
    user.save()
    assign_role(user, 'supplier_user')
    user.plain_text_password = password
    return user

#--------------------------------------/ getcsrf


@pytest.fixture
def get_csrf_token(client):
    return client.get(reverse('get_csrf_token'))

def test__get_csrf_token(get_csrf_token):
    assert get_csrf_token.status_code == 200
    assert_iqual(get_csrf_token.content, b'"The CSRF cookie was sent"')

#--------------------------------------/ Login

@pytest.fixture
def login_fail__without_credentials(client):
    return client.post(reverse('login'))

def test__login_fail__without_credentials(login_fail__without_credentials):
    assert login_fail__without_credentials.status_code == 400 # Error: Bad Request
    assert_json_equal(login_fail__without_credentials.content,
        {
          "username": [
            "This field is required."
          ],
          "password": [
            "This field is required."
          ]
        }
    )

@pytest.fixture
def login_successful__operator(client, operator_user):
    return client.post(reverse('login'), {'username': operator_user.username, 'password': operator_user.plain_text_password}, format='json')

def test__login_successful__operator(login_successful__operator, operator_user):
    assert login_successful__operator.status_code == 200
    assert_json_equal(login_successful__operator.content,
        {
            "username": operator_user.username,
            "email": operator_user.email,
            "supplier_company": None,
            "roles": ["operator"],
            "permissions": [
                "create_payment", 
                "get_payment", 
                "get_supplier", 
                "request_payment_anticipation",
                "update_payment", 
            ],
        }
    )


@pytest.fixture
def login_successful__supplier(client, supplier_user):
    return client.post(reverse('login'), {'username': supplier_user.username, 'password': supplier_user.plain_text_password}, format='json')

def test__login_successful__supplier(login_successful__supplier, supplier_user):
    assert login_successful__supplier.status_code == 200
    assert_json_equal(login_successful__supplier.content,
        {
            "username": supplier_user.username,
            "email": supplier_user.email,
            "supplier_company": supplier_user.supplier_company_id,
            "roles": ["supplier_user"],
            "permissions": [
                "get_payment", 
                "request_payment_anticipation",
            ],
        }
    )

@pytest.fixture
def authenticated_user_tries_to_login(client_with_logged_operator_user):
    return client_with_logged_operator_user.post(reverse('login'), {'username': 'some_username', 'password': 'somepassword123'}, format='json')

def test__authenticated_user_tries_to_login__response(authenticated_user_tries_to_login):
    assert authenticated_user_tries_to_login.status_code == 200
    assert_iqual(authenticated_user_tries_to_login.content,
        b'"User is already authenticated"'
    )

##  --------------------------------------/ Own Profile

@pytest.fixture
def own_profile__operator(client_with_logged_operator_user):
    return client_with_logged_operator_user.get(reverse('own_profile'))

def test__own_profile__operator(own_profile__operator):
    assert own_profile__operator.status_code == 200
    assert_json_equal(own_profile__operator.content,
        {
            "username": "test_operator_user",
            "email": "test@operator_user.anything",
            "supplier_company": None,
            "roles": ["operator"],
            "permissions": [
                "create_payment", 
                "get_payment", 
                "get_supplier", 
                "request_payment_anticipation",
                "update_payment", 
            ],
        }
    )


@pytest.fixture
def own_profile__supplier_user(client_with_logged_supplier_user):
    return client_with_logged_supplier_user.get(reverse('own_profile'))

def test__own_profile__supplier_user(own_profile__supplier_user, logged_supplier_user):
    assert own_profile__supplier_user.status_code == 200
    assert_json_equal(own_profile__supplier_user.content,
        {
            "username": "test_supplier_user",
            "email": "test@supplier_user.anything",
            "supplier_company": logged_supplier_user.supplier_company_id,
            "roles": ["supplier_user"],
            "permissions": [
                "get_payment", 
                "request_payment_anticipation",
            ],
        }
    )

@pytest.fixture
def own_profile_fail(client):
    return client.get(reverse('own_profile'))

def test__own_profile_fail__without_credentials(own_profile_fail):
    assert own_profile_fail.status_code == 403 # Error: Forbidden
    assert_json_equal(own_profile_fail.content,
        {
          "detail": "Authentication credentials were not provided."
        }
    )

##--------------------------------------/ Logout

@pytest.fixture
def logout_successful(client_with_logged_operator_user):
    return client_with_logged_operator_user.post(reverse('logout'))

def test__logout_successful(logout_successful):
    assert logout_successful.status_code == 200
    assert_iqual(logout_successful.content, b'"Logged out"')

@pytest.fixture
def logout_fail__credentials_were_not_provided(client):
    return client.post(reverse('logout'))

def test__logout_fail__credentials_were_not_provided(logout_fail__credentials_were_not_provided):
    assert logout_fail__credentials_were_not_provided.status_code == 403 #Forbidden
    assert_json_equal(logout_fail__credentials_were_not_provided.content,
        {
          "detail": "Authentication credentials were not provided."
        }
    )
