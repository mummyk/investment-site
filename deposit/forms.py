from django import forms
from .models import Deposit


class DepositForm(forms.ModelForm):
    amount = forms.FloatField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg','type':'number', 'placeholder': 'Enter amount'}))

    class Meta:
        model = Deposit
        managed = True
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'
        fields = ['amount']


