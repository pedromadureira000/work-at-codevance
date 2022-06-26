from django.urls import path
from .views import (
    OwnProfileView, Login, Logout, GetCSRFToken
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    #Auth
    path('login', Login.as_view()),
    path('logout', Logout.as_view()),
    path('getcsrf', GetCSRFToken.as_view()),
    #User
    path('own_profile', OwnProfileView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
