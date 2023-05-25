from django.shortcuts import render, redirect
from yahoofinancials import YahooFinancials as yf
from django.contrib.auth.decorators import login_required
from .models import  Withdrawal
from deposit.models import Deposit
from django.db.models import Sum
from django.contrib import messages
import urllib.request
from .forms import WithdrawalForm
from general.models import Profit
from django.conf import settings

@login_required
def withdraw_transaction(request):
    btcRate = 0.00
    ethRate = 0.00
    account_balance = 0.00
    withdraw_history = 0.00
    total_withdraw = 0.00
    total_actual_withdraw = 0.00
    total_withdraw_pending_arg = 0.00
    total_withdraw_rejected_arg = 0.00
    site_name = settings.SITE_NAME

    # Get all deposit, withdraws and profit
    if Withdrawal.objects.filter(user=request.user).exists():
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

        # get total deposit and withdraws that are not pending
        actual_deposit = deposit.filter(
            user=request.user, pending=False).aggregate(Sum('amount'))
        total_actual_deposit = actual_deposit['amount__sum']
        
        actual_withdraw = withdraw.filter(
            user=request.user, pending=False).aggregate(Sum('amount'))
        total_actual_withdraw = actual_withdraw['amount__sum']

        # total pending depoist and withdrawal
        total_deposit_pending = deposit.filter(
            user=request.user, pending=True)
        total_withdraw_pending = withdraw.filter(
            user=request.user, pending=True)

        # total rejected deposit and withdraw
        total_deposit_rejected = deposit.filter(
            user=request.user, rejected=True)
        total_withdraw_rejected = withdraw.filter(
            user=request.user, rejected=True)

        # aggregate for all pending, rejected and actual
        # pending
        deposit_pending_arg = total_deposit_pending.aggregate(
            Sum('amount'))
        total_deposit_pending_arg = deposit_pending_arg['amount__sum']
        
        withdraw_pending_arg = total_withdraw_pending.aggregate(
            Sum('amount'))
        total_withdraw_pending_arg = withdraw_pending_arg['amount__sum']

        # rejected
        deposit_rejected_arg = total_deposit_rejected.aggregate(
            Sum('amount'))
        total_deposit_rejected_arg = deposit_rejected_arg['amount__sum']
        
        withdraw_rejected_arg = total_withdraw_rejected.aggregate(
            Sum('amount'))
        total_withdraw_rejected_arg = withdraw_rejected_arg['amount__sum']
        
        account_balance = get_balance(request)
       
        

     # Your total profit
    if Profit.objects.all().exists():
        first_deposit = deposit.filter(
            user=request.user, pending=False).first()
        profit = Profit.objects.all()
        first_day = first_deposit.created
        # add the profit from the day of the first deposit
        user_total_profit = profit.filter(
            created__gte=first_day).aggregate(Sum('amount'))

        # get total available profit and total actual deposit
        available_balance = total_actual_deposit['amount__sum'] + \
            (total_actual_deposit['amount__sum'] *
            (user_total_profit['amount__sum']/100))

    # Crypto rate
    if connect():
        try:
            cryptocurrencies = ['BTC-USD', 'ETH-USD']
            crypto = yf(cryptocurrencies)
            yc = crypto.get_current_price()
            btcRate = yc['BTC-USD']+(yc['BTC-USD']*0.01)
            ethRate = yc['ETH-USD']+(yc['ETH-USD']*0.1)
        except:
            messages.error(request, 'Could not get current price')
    else:
        messages.error(request, 'You are offline')

    # withdrawal form
    form = WithdrawalForm(request.POST or None)

    context = {'title': 'Withdraw', 'withdraws': True, 'data': withdraw_history, "balance": get_balance(request),
               'total_withdraw': total_withdraw, 'actual_withdraw': total_actual_withdraw,
               'total_pending': total_withdraw_pending_arg, 'total_rejected': total_withdraw_rejected_arg,
               'form': form, 'btcRate': btcRate, 'ethRate': ethRate,"site_name":site_name
               }

    return render(request, 'withdraws/withdraw.html', context)
 
@login_required
def withdrawForm(request):
    # get available balance

    form = WithdrawalForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            balance = get_balance(request)
            amount = float(form['amount'].value())
            if amount <= balance:
                withdraw = form.save(commit=False)
                withdraw.user = request.user
                withdraw.save()
                megs = messages.success(
                    request, 'Withdraw successful and pending')
                return redirect('/withdraws', megs)
            else:
                megs = messages.success(
                    request, 'Insufficient funds, Top_up is required')
                return redirect('/deposit', megs)
        else:
            meg = messages.error(request, 'You have low balance, Top up')
            return redirect('/deposits', meg)


def connect():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False
     
@ login_required
def get_balance(request):
    total_profit = 0.00
    total_deposit = 0.00
    total_withdraw = 0.00
    available_balance = 0.00
    user_total_profit = 0.00
    available_balance_and_profit = 0.00
    # get date of the first deposit
    if Deposit.objects.all().exists() or Withdrawal.objects.all().exists:
        deposit = Deposit.objects.all()
        deposit = deposit.filter(user=request.user,  pending = False, rejected = False)
        withdraw = Withdrawal.objects.all()
        withdraw = withdraw.filter(user=request.user,  pending = False, rejected = False)
        first_deposit = deposit.first()
        
        # get total deposit and withdraw
        total_deposit = deposit.aggregate(Sum('amount'))
        total_withdraw = withdraw.aggregate(Sum('amount'))
        
        # get the available balance
        if deposit:
            available_balance = {
                key: abs(total_deposit[key]-total_withdraw[key]) for key in total_deposit}
        # profit from the day of deposit
        if Profit.objects.all().exists():
            profit = Profit.objects.all()
            first_day = first_deposit.created
            # add the profit from the day of the first deposit
            profits = profit.filter(created__gte=first_day)
            user_total_profit = profits.aggregate(Sum('amount'))
            available_balance_and_profit = available_balance['amount__sum'] * \
                (user_total_profit['amount__sum']/100)
            available_balance = available_balance['amount__sum'] + \
                available_balance_and_profit

    else:
        messages.error(request, "No deposit")

    return available_balance