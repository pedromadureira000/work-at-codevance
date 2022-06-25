from django.urls import path
from .views import (
    ObtainAuthToken, OwnProfileView, Login, Logout, GetCSRFToken
)

urlpatterns = [
    #Auth
    path('login', Login.as_view()),
    path('logout', Logout.as_view()),
    path('getcsrf', GetCSRFToken.as_view()),
    #User
    path('own_profile', OwnProfileView.as_view()),
    path('gettoken', ObtainAuthToken.as_view(), name='gettoken'),
]
