from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.text import gettext_lazy as _

from .models import *


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password','tokens']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid Credentials, Please enter valid details.')
        if not user.is_active:
            raise AuthenticationFailed('Your account is inactive, Please contact admin.')
        return {


            'email': user.email,
            'password': user.password,
            'tokens': user.tokens()
        }

        return super().validate(attrs)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }


    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
