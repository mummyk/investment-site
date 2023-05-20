from django.contrib import admin
from .models import Deposit, Wallet

# Register your models here.
admin.site.register(Deposit)
admin.site.register(Wallet)