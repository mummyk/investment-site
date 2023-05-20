from django import forms
from .models import Withdrawal

class WithdrawalForm(forms.ModelForm):
    amount = forms.FloatField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'title flex-1 w-full p-4  bg-gray-200 rounded-xl', 'placeholder': 'Enter amount'}))
    wallet = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'title flex-1 w-full p-4 my-4 bg-gray-200 rounded-xl', 'placeholder': 'Enter Your wallet'}))

    class Meta:
        model = Withdrawal
        managed = True
        verbose_name = 'withdrawal'
        verbose_name_plural = 'withdrawals'
        fields = ['amount', 'wallet']
