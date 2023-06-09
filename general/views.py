from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.decorators import verified_email_required
from django.conf import settings
from deposit.models import Wallet, Deposit
from withdraw.models import Withdrawal
from income.models import Profit,Withdrawable
from django.db.models import Sum
from django.contrib import messages

# Create your views here.
@login_required
@verified_email_required
def dashboard(request):
   site_name = settings.SITE_NAME
   context = {"title":"Dashboard", "site_name":site_name}
   return render(request, "general/dashboard/dashboard.html", context)


def termsAndCondition(request):
   context = {"title":'Terms & Conditions'}
   return render(request, "general/t&c.html")

@login_required
def transactions(request):
    # Get all deposit, withdraws and profit
    balance = 0.0
    site_name = settings.SITE_NAME
    total_actual_deposit = 0.00
    total_deposit = 0.00
    total_deposit_pending = 0.00
    total_transactions = 0.00
    deposit_history = 0.00
    withdraw_history = 0.00
    user_total_profit = 0.00
    profit = 0.00
    total_withdraw = 0.00
    profits = 0.00
    user_total_profit = 0.00
    last_profit = 0.00
    total_actual_withdraw = 0.00
    user_withdrawable_amount = 0.00

    if Deposit.objects.filter(user=request.user).exists() or Withdrawal.objects.filter(user=request.user).exists():
        deposit = Deposit.objects.all()
        withdraw = Withdrawal.objects.all()

        # history
        deposit_history = deposit.filter(user=request.user)
        withdraw_history = withdraw.filter(user=request.user)

        # total of all deposits and withdraw
        all_deposit = deposit_history.aggregate(Sum('amount'))
        total_deposit = all_deposit['amount__sum']
        
        all_withdraw = withdraw_history.aggregate(Sum('amount'))
        total_withdraw = all_withdraw['amount__sum']

        # get total deposit that are not pending
        actual_deposit = deposit.filter(
            user=request.user, pending=False, rejected=False).aggregate(Sum('amount'))
        total_actual_deposit = actual_deposit['amount__sum']
        
        actual_withdraw = withdraw.filter(
            user=request.user, pending=False, rejected=False).aggregate(Sum('amount'))
        total_actual_withdraw = actual_withdraw['amount__sum']

        # total pending depoist and withdrawal
        deposit_pending = deposit.filter(
            user=request.user, pending=True).aggregate(Sum('amount'))
        total_deposit_pending = deposit_pending['amount__sum']
        
        withdraw_pending = withdraw.filter(
            user=request.user, pending=True).aggregate(Sum('amount'))
        total_withdraw_pending = withdraw_pending['amount__sum']

        # total rejected deposit and withdraw
        deposit_rejected = deposit.filter(
            user=request.user, rejected=True).aggregate(Sum('amount'))
        total_deposit_rejected = deposit_rejected['amount__sum']
        
        withdraw_rejected = withdraw.filter(
            user=request.user, rejected=True).aggregate(Sum('amount'))
        total_withdraw_rejected = withdraw_rejected['amount__sum']

        
        if total_actual_deposit is None:
            total_actual_deposit = 0.00
        if total_actual_withdraw is None:
            total_actual_withdraw = 0.00

     # Your total profit
    if Profit.objects.all().exists():
        # Get Withdrawable
        if Withdrawable.objects.filter(user=request.user).exists():
            withdrawable =  Withdrawable.objects.all()
            user_withdrawable = withdrawable.filter(user=request.user)
            user_withdrawable_arg = user_withdrawable.aggregate(Sum('profit_amount'))
            user_withdrawable_amount = user_withdrawable_arg['profit_amount__sum']
            # First withdrawable
            first_withdrawable = user_withdrawable.first()
            
            
            profit = Profit.objects.all()
            first_day = first_withdrawable.created
            profits = profit.filter(
                created__gte=first_day)
            last_profit = profit.last()
            # add the profit from the day of the first deposit
            total_profit = profit.aggregate(Sum('amount'))
            user_total_profit = total_profit['amount__sum']
                    
            if user_total_profit is None:
                user_total_profit = 0.00
        
        # Total Approved Transactions
        balance = total_actual_deposit + user_withdrawable_amount

    context = {'title': 'Transactions', 'deposit': total_deposit, 'balance': balance,
               'withdraw': total_withdraw, 'total_profit': user_total_profit, 'profit': profits, "user_total_profit":user_total_profit,
               'deposits': deposit_history, 'withdraws': withdraw_history, 'transactions': True, "site_name":site_name, "last_profit":last_profit, "total_actual_deposit":total_actual_deposit, "total_actual_withdraw":total_actual_withdraw,
               }

    return render(request, 'transaction/transactions.html', context)



