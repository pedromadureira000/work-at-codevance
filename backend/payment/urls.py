from django.urls import path
from .views import (
    PaymentView,
    RequestAnticipation,
    SpecificPaymentView,
    PaymentHistoryView,
)

app_name = 'payment'
urlpatterns = [
    path('payment', PaymentView.as_view(), name="get_or_post_payment"),
    path('payment/<payment_id>', SpecificPaymentView.as_view(), name="update_payment"),
    path('request_anticipation/<payment_id>', RequestAnticipation.as_view(), name="request_anticipation"),
    path('payment_history/<payment_id>', PaymentHistoryView.as_view(), name="payment_history"),

]

