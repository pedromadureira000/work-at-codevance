from rolepermissions.roles import AbstractUserRole

class Operator(AbstractUserRole):
    available_permissions = {
        #  "create_supplier": True,
        #  "get_supplier": True,
        #  "update_supplier": True,
        #  "delete_supplier": True,
        #  "create_supplier_user": True,
        #  "get_supplier_user": True,
        #  "update_supplier_user": True,
        #  "delete_supplier_user": True,
        "create_payment": True,
        "get_payment": True,
        "update_payment": True,
        #  "delete_payment": True,
    }

class SupplierUser(AbstractUserRole):
    available_permissions = {
        "get_payment": True,
        "request_payment_anticipation": True,
    }
