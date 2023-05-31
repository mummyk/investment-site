from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
from datetime import datetime, timedelta

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
     

"""  def save(self, *args, **kwargs):
        self.start = datetime.now()
        pack = Package.objects.all()
        pack = pack.get(name=self.packages)
        self.end = self.start+timedelta(pack.duration)
        return super().save(*args, **kwargs) """


class MinMax(models.Model):
    minimum_deposit = models.IntegerField(_("Minimum Deposit"))
    maximum_deposit = models.IntegerField(_("Maximum Deposit"))
    minimum_withdraw = models.IntegerField(_("Minimum Withdraw"))
    maximum_withdraw = models.IntegerField(_("Minimum Withdraw"))
    created = models.DateTimeField(_('Created'), auto_now_add=True,)
    
    def __str__(self):
        return self.created.strftime('%A')