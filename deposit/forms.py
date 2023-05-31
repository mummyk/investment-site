from django import forms
from .models import Deposit


class DepositForm(forms.ModelForm):
    amount = forms.FloatField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg','type':'number', 'placeholder': 'Enter amount'}))
    wallet = forms.ChoiceField(choices=Deposit.WALLET_TYPE,
                               label="", widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'placeholder': 'Select Gender'}))
    class Meta:
        model = Deposit
        fields = ['amount', 'wallet']


class TransactionID(forms.ModelForm):
    transaction_id = forms.CharField(label='',widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg','type':'text', 'placeholder': 'Enter Transaction ID'}))
    class Meta:
        model = Deposit
        fields = ['transaction_id']
