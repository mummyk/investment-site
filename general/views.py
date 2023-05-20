from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.account.decorators import verified_email_required
from django.conf import settings
from deposit.models import Wallet, Deposit
from withdraw.models import Withdrawal

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

    if Deposit.objects.filter(user=request.user).exists() or Withdrawal.objects.filter(user=request.user).exists():
        deposit = Deposit.objects.all()
        withdraw = Withdrawal.objects.all()

        # history
        deposit_history = deposit.filter(user=request.user)
        withdraw_history = withdraw.filter(user=request.user)

        # total of all deposits and withdraw
        total_deposit = deposit.filter(
            user=request.user).aggregate(Sum('amount'))
        total_withdraw = withdraw.filter(
            user=request.user).aggregate(Sum('amount'))

        # get total deposit that are not pending
        total_actual_deposit = deposit.filter(
            user=request.user, pending=False).aggregate(Sum('amount'))

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
        total_deposit_pending_arg = total_deposit_pending.aggregate(
            Sum('amount'))
        total_withdraw_pending_arg = total_withdraw_pending.aggregate(
            Sum('amount'))

        # rejected
        total_deposit_rejected_arg = total_deposit_rejected.aggregate(
            Sum('amount'))
        total_withdraw_rejected_arg = total_withdraw_rejected.aggregate(
            Sum('amount'))

        total_transactions = {
            key: abs(total_deposit[key]+total_withdraw[key]) for key in total_deposit}
    else:
        total_actual_deposit = 0.00
        total_deposit = 0.00
        total_deposit_pending = 0.00
        total_transactions = 0.00
        deposit_history = 0.00
        withdraw_history = 0.00
        user_total_profit = 0.00
        profit = 0.00
        total_withdraw = 0.00

     # Your total profit
    if Profit.objects.all().exists():
        first_deposit = deposit.filter(
            user=request.user, pending=False).first()
        profit = Profit.objects.all()
        first_day = first_deposit.created
        profits = profit.filter(
            created__gte=first_day)
        # add the profit from the day of the first deposit
        user_total_profit = profit.filter(
            created__gte=first_day).aggregate(Sum('amount'))

    context = {'title': 'Transactions', 'deposit': total_deposit['amount__sum'], 'balance': total_transactions['amount__sum'],
               'withdraw': total_withdraw['amount__sum'], 'total_profit': user_total_profit['amount__sum'], 'profit': profits,
               'deposits': deposit_history, 'withdraws': withdraw_history, 'transactions': True,"site_name":site_name
               }

    return render(request, 'dashboard_pay.html', context)
