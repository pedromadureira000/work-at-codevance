from rolepermissions.roles import AbstractUserRole

class Operator(AbstractUserRole):
    available_permissions = {
        "get_supplier": True,
        "create_payment": True,
        "get_payment": True,
        "update_payment": True,
        "request_payment_anticipation": True,
    }

class SupplierUser(AbstractUserRole):
    available_permissions = {
        "get_payment": True,
        "request_payment_anticipation": True,
    }
