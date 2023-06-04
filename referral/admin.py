from django.contrib import admin
from .models import ReferralModel, Ref_withdrawal, Ref_deposit, Referral_percentage

# Register your models here.
admin.site.register(ReferralModel)
admin.site.register(Ref_withdrawal)
admin.site.register(Ref_deposit)
admin.site.register(Referral_percentage)