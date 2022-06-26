from django.urls import path
from .views import (
    SupplierCompanyView
)

urlpatterns = [
    path('supplier_company', SupplierCompanyView.as_view()),
]
