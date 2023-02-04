from django.contrib.auth.base_user import *
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class TestSubjectManager(BaseUserManager):
    def _create_user(self, password, email, first_name, last_name, **extra_params):
        if not email:
            raise ValueError("Email must be provided")
        if not password and password_validation.validate_password(password):
            raise ValueError("Password must be set")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            **extra_params
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, email, first_name, last_name, **extra_params):
        extra_params.setdefault('is_staff', True)
        extra_params.setdefault('is_active', True)
        extra_params.setdefault('is_superuser', True)
        return self._create_user(password, email, first_name, last_name, **extra_params)

    def create_user(self, password, email, first_name, last_name, **extra_params):
        extra_params.setdefault('is_staff', False)
        extra_params.setdefault('is_active', True)
        extra_params.setdefault('is_superuser', False)
        return self._create_user(password, email, first_name, last_name, **extra_params)


class TestSubject(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=155, blank=True)
    email = models.EmailField(blank=False, db_index=True, unique=True)

    school = models.CharField(max_length=255, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = TestSubjectManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "Test Subject"
        verbose_name_plural = "Test Subjects"
