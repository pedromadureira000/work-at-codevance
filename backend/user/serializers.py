from typing import OrderedDict
from rest_framework import serializers
from .models import User
from rolepermissions.roles import get_user_roles
from django.utils.translation import gettext_lazy as _


#-------------------------------------------------/Auth Serializers

class SwaggerLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

class SwaggerProfilePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    current_password = serializers.CharField(write_only=True)

class UpdateOwnEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email'] 

#------------------------------------------------------/User serializers

class UserResponseSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField() 

    class Meta:
        model = User
        fields = ['username', 'email', 'supplier_company', 'roles', 'permissions']

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


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField() 

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'supplier_company', 'roles', 'permissions']
        extra_kwargs = {
            'password': {'write_only': True},
        }

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
