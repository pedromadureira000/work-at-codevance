from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg import openapi
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UpdateOwnEmailSerializer, UserResponseSerializer, UserSerializer, SwaggerLoginSerializer
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from settings.response_templates import error_response, serializer_invalid_response, unknown_exception_response
from rest_framework.decorators import action

#------------------------/ Auth Views

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        return Response(_("The CSRF cookie was sent"))

class Login(APIView):
    permission_classes = (permissions.AllowAny,)
    @swagger_auto_schema(request_body=SwaggerLoginSerializer, method='post', responses={200: UserResponseSerializer}) 
    @action(detail=False, methods=['post'])
    def post(self, request):
        if request.user.is_authenticated:
            return Response(_("User is already authenticated"))
        serializer = SwaggerLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data["username"], password=serializer.validated_data["password"], request=request)
            if user is not None:
                login(request, user)
                return Response(UserSerializer(user).data)
            else:
                return error_response(detail=_("The login failed"), status=status.HTTP_401_UNAUTHORIZED)
        return serializer_invalid_response(serializer.errors)

class Logout(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            logout(request)
            return Response(_('Logged out'))
        except Exception as error:
            unknown_exception_response(action=_('log out'))

#-------------------------------------------/ Users Views / -------------------------------------
class OwnProfileView(APIView):
    @swagger_auto_schema(method='get', responses={200: UserResponseSerializer}) 
    @action(detail=False, methods=['get'])
    def get(self, request):
        try:
            data = UserSerializer(request.user).data
            return Response(data)
        except Exception as error:
            #  print(error)
            return unknown_exception_response(action=_('get request user profile'))

    @swagger_auto_schema(request_body=UpdateOwnEmailSerializer, responses={200: 'Email changed with success.'})
    @transaction.atomic
    def put(self, request):
        serializer = UpdateOwnEmailSerializer(request.user, data=request.data, context={"request": request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response("Email changed with success.")
            except Exception as error:
                print(error)
                return unknown_exception_response(action=_('update request user profile'))
        return serializer_invalid_response(serializer.errors)

