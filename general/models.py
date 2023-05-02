from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

# Create your models here.

# model for plans
class Packages():
   PLAN_TYPE = ((_('Basic'), 'Basic'),
                     (_('Copper'), 'Copper'),
                     (_('Investor'), 'Investor'),
                     (_('Shark'), 'Shark'),
                     (_('Whale'), 'Whale'))
  
   packages = models.CharField(_("Plan Type"), max_length=50, choices=PLAN_TYPE)
   description = models.CharField(_('Description'),)
   amount = models.FloatField(_("Amount"),)
   created = models.DateTimeField(_('Created'), auto_now_add=True,)
   
   def __str__(self):
        return self.packages
