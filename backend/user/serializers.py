from typing import OrderedDict
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User
from rolepermissions.roles import get_user_roles
from rolepermissions.roles import assign_role
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.validators import UniqueTogetherValidator


#-------------------------------------------------/Auth Serializers

class SwaggerLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

class SwaggerProfilePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    current_password = serializers.CharField(write_only=True)

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

#------------------------------------------------------/User serializers

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField() 

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'supplier_company', 'roles', 'permissions']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    #  def validate(self, attrs):
        #  if self.context['request'].method == 'PUT':
            #  pass
        #  return attrs

    def get_roles(self, user):
        # If "user" is OrderedDict. This means receive data and not receive instance.
        # If "user" is model.User. This means we receive a instance.
        if isinstance(user, OrderedDict):
            roles = []
            return roles
        roles = []
        user_roles = get_user_roles(user) 
        for role in user_roles:
            roles.append(role.get_name())
        return roles

    def get_permissions(self, user):
        if isinstance(user, OrderedDict):
            permissions_list = []
            return permissions_list 
        permissions = user.user_permissions.all()
        permissions_list = [perm.codename for perm in permissions]
        return permissions_list 

#  class SupplierUserPOSTSerializer(UserSerializer):
    #  def create(self, validated_data):  
        #  username = validated_data['username']
        #  email = validated_data['email']
        #  password=validated_data['password']
        #  user = User.objects.create_user(username, password, email=email, supplier_company=validated_data['supplier_company'])
        #  assign_role(user, 'supplier_user')
        #  return user

#  class SupplierUserPUTSerializer(UserSerializer):
    #  class Meta:
        #  model = User
        #  fields = ['username', 'first_name', 'last_name', 'email', 'status',
                #  'roles', 'permissions', 'contracting_code', 'user_code', 'note']
        #  read_only_fields = ['username', 'user_code']

