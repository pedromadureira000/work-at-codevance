from django.urls import path
from .views import (
    PaymentView,
    RequestAnticipation,
    SpecificPaymentView,
    PaymentHistoryView,
)

app_name = 'payment'
urlpatterns = [
    path('payment', PaymentView.as_view()),
    path('payment/<payment_id>', SpecificPaymentView.as_view()),
    path('request_anticipation/<payment_id>', RequestAnticipation.as_view()),
    path('payment_history/<payment_id>', PaymentHistoryView.as_view()),

]

