from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import re
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Withdrawal(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "Users_info"), on_delete=models.CASCADE)
    wallet = models.CharField(_("Wallet ID"), max_length=200)
    amount = models.FloatField(_("Amount"))
    pending = models.BooleanField(_("Pending Transactions"), default=True)
    rejected = models.BooleanField(
        _("Rejected/Canceled Transactions"), default=False)
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    def __str__(self):
        return self.user.email + '--' + self.created.strftime('%A')

    def save(self, *args, **kwargs):

        # For all possible BTC & ETH wallet configuration
        BTC_ADDRESS_MATCH = '([13]{1}[a-km-zA-HJ-NP-Z1-9]{27,34}|bc1[a-z0-9]{39,59})'
        ETH_ADDRESS_MATCH = '0x[a-fA-F0-9]{40}'

        # matching btc address
        btc = re.match(BTC_ADDRESS_MATCH, self.wallet)
        eth = re.match(ETH_ADDRESS_MATCH, self.wallet)

        return super().save(*args, **kwargs)