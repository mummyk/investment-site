from django.shortcuts import render, redirect
from yahoofinancials import YahooFinancials as yf
from django.contrib.auth.decorators import login_required
from .models import  Withdrawal
from deposit.models import Deposit
from django.db.models import Sum
from django.contrib import messages
import urllib.request
from .forms import WithdrawalForm
from income.models import Profit
from django.conf import settings
from helper.views import getBalance

@login_required
def withdraw_transaction(request):
    balance = 0.00
    withdraw_history = 0.00
    total_withdraw = 0.00
    total_actual_withdraw = 0.00
    total_withdraw_pending = 0.00
    total_withdraw_rejected = 0.00
    site_name = settings.SITE_NAME

    # Get all deposit, withdraws and profit
    if Withdrawal.objects.filter(user=request.user).exists():
        withdraw = Withdrawal.objects.all()

        # history
        withdraw_history = withdraw.filter(user=request.user)

        # total of all deposits and withdraw
        all_withdraw = withdraw_history.aggregate(Sum('amount'))
        total_withdraw = all_withdraw['amount__sum']

        # get total deposit and withdraws that are not pending
        actual_withdraw = withdraw.filter(
            user=request.user, pending=False).aggregate(Sum('amount'))
        total_actual_withdraw = actual_withdraw['amount__sum']

        # total pending depoist and withdrawal
        withdraw_pending = withdraw.filter(
            user=request.user, pending=True).aggregate(
            Sum('amount'))
        total_withdraw_pending = withdraw_pending['amount__sum']

        # total rejected deposit and withdraw
        total_withdraw_rejected = withdraw.filter(user=request.user, rejected=True).aggregate(Sum('amount'))

        # aggregate for all pending, rejected and actual
        # pending
        balance = getBalance(request)

    # withdrawal form
    context = {'title': 'Withdraw', 'withdraws': True, 'data': withdraw_history, "balance": balance,
               'total_withdraw': total_withdraw, 'actual_withdraw': total_actual_withdraw,
               'total_pending': total_withdraw_pending , 'total_rejected': total_withdraw_rejected,
                "site_name":site_name
               }

    return render(request, 'withdraws/withdraw.html', context)
 
@login_required
def withdrawForm(request):
    
    site_name = settings.SITE_NAME
    
    # get available balance
    form = WithdrawalForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            balance = getBalance(request)
            amount = float(form['amount'].value())
            if amount <= balance - 3:
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
    
    context = {'form': form, 'title': 'Withdraw', "site_name":site_name,}
    return render(request, 'withdraws/withdraw_form.html', context)


@login_required
def confirmWithdraw(request, withdraw_id):
    site_name = settings.SITE_NAME
    withdraws = Withdrawal.objects.all()
    
    #get the amount from the last saved form
    recent_withdraws = withdraws.get(user=request.user, id=withdraw_id)
    
    context = {'title':'Confirm withdraws', "site_name":site_name, 'recent_withdraws':recent_withdraws, "withdraw_id":withdraw_id, 'form':form}
    return render(request, 'withdraws/confirm_withdraws.html', context)

@login_required
def cancelTransaction(request, withdraw_id):
    withdraw = Withdrawal.objects.all()
    #get the amount from the last saved form
    recent_withdraw = withdraw.get(user=request.user, id=withdraw_id)
    recent_withdraw.rejected = True
    recent_withdraw.pending = False
    recent_withdraw.save()
    return redirect(to='/withdraws')

@login_required
def withdrawDetails(request, withdraw_id):
    site_name = settings.SITE_NAME
    
    withdraws = Withdrawal.objects.all()
    withdrawal_details = withdraws.filter(user=request.user, id=withdraw_id)
    
    
    context={'title':'Withdrawal Details', "site_name":site_name, 'details':withdrawal_details}
    return render(request, 'withdraws/withdraw_details.html', context)
    