from django.contrib import admin
from .models import Withdrawal, IsWithdrawalable

# Register your models here.
admin.site.register(Withdrawal)
admin.site.register(IsWithdrawalable)
