from django import forms
from .models import Deposit


class DepositForm(forms.ModelForm):
    amount = forms.FloatField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'title flex-1 w-full px-4 py-3 bg-gray-200 rounded-xl', 'placeholder': 'Enter amount'}))

    class Meta:
        model = Deposit
        managed = True
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'
        fields = ['amount']


