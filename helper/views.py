from django.shortcuts import render
from deposit.models import Deposit
from withdraw.models import Withdrawal
from income.models import Profit,Withdrawable
from django.db.models import Sum

# Create your views here.


def handle_400_error(request, exception):
    return render(request, "helper/400.html")


def handle_403_error(request, exception):
    return render(request, "helper/403.html")


def handle_404_error(request, exception):
    return render(request, "helper/404.html")


def handle_500_error(request):
    return render(request, "helper/500.html")


def getBalance(request):
    balance = 0.00    
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
        balance = (total_actual_deposit + user_withdrawable_amount)-total_actual_withdraw
        
    return balance
