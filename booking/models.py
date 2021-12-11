from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):

    def _create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('This email address must be set')

        if not password:
            raise ValueError('This password must be set')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)


ROLE_CHOICES = (
    (1, 'Manager'),
    (2, 'Employee')
)


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    USERNAME_FIELD = 'email'
    role = models.CharField(choices=ROLE_CHOICES, max_length=100, default='Employee')
    REQUIRED_FIELDS = ()

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id']

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class ParkingSpace(models.Model):
    name = models.CharField(max_length=500, default='Front side parking space')

    def __str__(self):
        return self.name


class Reservation(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    reserved_by = models.ForeignKey('User', on_delete=models.CASCADE)
    parking_space = models.ForeignKey('ParkingSpace', on_delete=models.CASCADE)

    def __str__(self):
        return self.parking_space.name + ' reserved by:' + self.reserved_by.email
