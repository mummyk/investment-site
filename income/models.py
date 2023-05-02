from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

# Create your models here.

# User package
class UserPackage():
   user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
   package = models.CharField(_("User Packages"))
   
   def __str__(self):
        return self.user.email + " " + self.package
