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
    path('login', Login.as_view(), name="login"),
    path('logout', Logout.as_view(), name="logout"),
    path('getcsrf', GetCSRFToken.as_view(), name="get_csrf_token"),
    #User
    path('own_profile', OwnProfileView.as_view(), name="own_profile"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
