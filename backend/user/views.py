from django.db.models.deletion import ProtectedError
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg import openapi
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AuthTokenSerializer, UserSerializer, SwaggerLoginSerializer
from settings.utils import has_permission, has_role
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from settings.response_templates import error_response, not_found_response, serializer_invalid_response, protected_error_response, unknown_exception_response, unauthorized_response
from rest_framework.decorators import action
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token

#------------------------/ Auth Views

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    request_schema_dict = openapi.Schema(
        title="ObtainAuthToken request body",
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, 
                description=_("User's username"), example="some_username"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description=_("User's password"), example="SafePassword123"),
        }
    )

    response_schema_dict = openapi.Schema(
        title="ObtainAuthToken response",
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING, 
                description=_("The authentication token, which is used in the authentication header."),
                example="c0ecd5242e6ea8a61392e6449624227b47ce5ef6")
        }
    )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    @swagger_auto_schema(method='post', responses={200: response_schema_dict}, request_body=request_schema_dict) 
    @action(detail=False, methods=['post'])
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        return Response(_("The CSRF cookie was sent"))

class Login(APIView):
    permission_classes = (permissions.AllowAny,)
    @swagger_auto_schema(request_body=SwaggerLoginSerializer, method='post', responses={200: UserSerializer}) 
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
    @swagger_auto_schema(method='get', responses={200: UserSerializer}) 
    @action(detail=False, methods=['get'])
    def get(self, request):
        try:
            data = UserSerializer(request.user).data
            return Response(data)
        except Exception as error:
            #  print(error)
            return unknown_exception_response(action=_('get request user profile'))

#  class AdminAgentView(APIView):
    #  @swagger_auto_schema(method='get', responses={200: AdminAgentPOSTSerializer(many=True)}) 
    #  @action(detail=False, methods=['get'])
    #  def get(self, request):
        #  if has_permission(request.user, 'get_admin_agents'):
            #  user = request.user
            #  agents = User.objects.filter(Q(contracting_id=user.contracting_id), Q(groups__name='admin_agent'))
            #  return Response(AdminAgentPOSTSerializer(agents, many=True).data)
        #  return unauthorized_response
    #  @swagger_auto_schema(request_body=AdminAgentPOSTSerializer) 
    #  @transaction.atomic
    #  def post(self, request):
        #  if has_permission(request.user, 'create_admin_agent'):
            #  serializer = AdminAgentPOSTSerializer(data=request.data, context={"request":request})
            #  if serializer.is_valid():
                #  try:
                    #  serializer.save()
                    #  return Response(serializer.data)
                #  except Exception as error:
                    #  transaction.rollback()
                    #  return unknown_exception_response(action=_('create admin agent'))
            #  return serializer_invalid_response(serializer.errors)
        #  return unauthorized_response

#  class SpecificAdminAgent(APIView):
    #  @swagger_auto_schema(request_body=AdminAgentPUTSerializer) 
    #  @transaction.atomic
    #  def put(self, request, contracting_code, username):
        #  if has_permission(request.user, 'update_admin_agent'):
            #  pass
        #  return unauthorized_response
    #  @transaction.atomic  
    #  def delete(self, request, contracting_code, username):
        #  if has_permission(request.user, 'delete_admin_agent'):
            #  if contracting_code != request.user.contracting_id:
                #  return not_found_response(object_name=_('The admin agent'))
            #  user_code = contracting_code + "*" + username
            #  try:
                #  user = User.objects.get(user_code=user_code, groups__name='admin_agent')
            #  except User.DoesNotExist:
                #  return not_found_response(object_name=_('The admin agent'))
            #  try:
                #  user.delete()
                #  return Response(_("Admin agent deleted successfully"))
            #  except ProtectedError as er:
                #  return protected_error_response(object_name=_('admin agent'))
            #  except Exception as error:
                #  transaction.rollback()
                #  return unknown_exception_response(action=_('delete admin agent'))
        #  return unauthorized_response
