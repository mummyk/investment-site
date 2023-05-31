from django.contrib import admin
from .models import Profit, Bonus, Withdrawable

# Register your models here.
admin.site.register(Profit)
admin.site.register(Bonus)
admin.site.register(Withdrawable)
