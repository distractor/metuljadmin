from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


def validate_zipcode(value):
    digits = len(str(value))
    if digits != 4:
        raise ValidationError(u'Number does not have 4 digits.')


def validate_ss(value):
    digits = len(str(value))
    if digits != 13:
        raise ValidationError(u'Number does not have 13 digits.')


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only PDF supported.')


def modify_filename(instance, filename):
    return f"certificates/{timezone.now().year}/{instance.first_name}_{instance.last_name}.pdf"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Name.
    first_name = models.CharField(max_length=100, blank=False, default=None)
    last_name = models.CharField(max_length=100, blank=False, default=None)
    # Birthday.
    date_born = models.DateField(verbose_name="Birthday", blank=False, default=None)

    # Address
    street = models.CharField(max_length=250, blank=False, default=None)
    city = models.CharField(max_length=400, blank=False, default=None)
    zipcode = models.IntegerField(validators=[validate_zipcode], blank=False, default=None)
    # Contact.
    phone_number = PhoneNumberField(region="SI", blank=False, default=None)
    email = models.EmailField(_("email address"), unique=True)
    # Social Security Number.
    social_security_number = models.CharField(max_length=13, validators=[validate_ss],
                                              verbose_name="EMŠO", blank=False, default=None)
    # Licences.
    has_zpls = models.BooleanField(default=False, verbose_name='ZPLS')
    has_fai = models.BooleanField(default=False, verbose_name="FAI")
    antidoping_certificate = models.FileField(blank=True, null=True,
                                              upload_to=modify_filename,
                                              max_length=300, validators=[validate_file_extension])

    # Membership.
    wants_valid_membership = models.BooleanField(default=False, verbose_name="wants valid membership")
    paid_membership = models.BooleanField(default=False, verbose_name="paid membership")

    # Meta.
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
