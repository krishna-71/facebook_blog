from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def base_user_create_func(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Email is must to create an account.')
        email = self.normalize_email(email)
        now = timezone.now()
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            date_joined=now,
            last_login=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self.base_user_create_func(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self.base_user_create_func(email, password, True, True, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=245,default=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=155, default='hi')
    last_name = models.CharField(max_length=155, default='authentication')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
