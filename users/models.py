from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django_countries.fields import CountryField
from django.utils.translation import gettext as _

# Create your models here.


class UserInfoModel(models.Model):
    GENDER_CHOICE = (
        ("None", _("Select your gender")),
        ("MALE", _("Male")),
        ("FEMALE", _("Female")),
        ("OTHERS", _("Others")),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(_('Your Date of Birth'), null=True)
    gender = models.CharField(
        _('Your gender'), choices=GENDER_CHOICE, max_length=18)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Please enter your country code and your phone number.")
    phone_number = models.CharField(_('Your Phone Number'),
                                    validators=[phone_regex], max_length=17)
    address = models.CharField(
        _('Your address'), max_length=300)
    country = CountryField(
        _('Your country'), blank_label='(select your country)')
    state = models.CharField(
        _("Your State"), max_length=50)
    city = models.CharField(_("Your City"), max_length=50)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    def __str__(self):
        return self.user.username
