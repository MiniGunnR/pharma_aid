from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone

from utils.models import TimeStamped


class UserManager(BaseUserManager):

    def _create_user(self, email, password, mobile, first_name, last_name,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email, password, mobile, first name and last name.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, mobile=mobile, first_name=first_name, last_name=last_name,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, mobile=None, first_name=None, last_name=None, **extra_fields):
        return self._create_user(email, password, mobile, first_name, last_name, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, mobile, first_name, last_name, **extra_fields):
        return self._create_user(email, password, mobile, first_name, last_name, True, True,
                                 **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user class.
    """
    email = models.EmailField('Email Address', unique=True, max_length=50)
    mobile = models.CharField('Mobile Number', max_length=15)
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)

    is_staff = models.BooleanField('Staff Status', default=False)
    is_active = models.BooleanField('Active', default=True)
    is_admin = models.BooleanField('Admin Status', default=False)

    date_joined = models.DateTimeField('Date Joined', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile']

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Address(TimeStamped):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    address_name = models.CharField('Address Name', help_text='For example, home, office, etc.', max_length=100)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "{0} - {1}".format(self.user, self.address_name)


class AddressInfo(TimeStamped):
    address = models.OneToOneField(Address)
    name = models.CharField('Recipient Name', help_text='It could be your name or the name of someone who lives at this address.', max_length=50)
    address_1 = models.CharField('First line of address', max_length=50)
    address_2 = models.CharField('Second line of address', max_length=50, blank=True)
    city = models.CharField(max_length=50)
    zip = models.CharField('Zip Code', max_length=10)
    country = models.CharField(max_length=50)

    def __str__(self):
        return "{0} - Info".format(self.address)


class Profile(TimeStamped):
    user = models.OneToOneField(User)
    institution = models.CharField(max_length=255)
    department = models.CharField(max_length=255)

    def __str__(self):
        return "{user}'s profile".format(user=self.user)
