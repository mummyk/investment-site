from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from referral.models import ReferralModel
from .models import Wallet, Deposit
from .forms import DepositForm, TransactionID
from django.db.models import Sum
from django.contrib import messages
from django.conf import settings

# Create your views here.
@login_required
def deposit_transaction(request):
    site_name = settings.SITE_NAME
    
    # Get all deposit, withdraws and profit
    if Deposit.objects.filter(user=request.user).exists():
        deposit = Deposit.objects.all()

        # history
        deposit_history = deposit.filter(user=request.user)

        # total of all deposits and withdraw
        all_deposit = deposit_history.aggregate(Sum('amount'))
        total_deposit = all_deposit['amount__sum']

        # get total deposit that are not pending
        actual_deposit = deposit.filter(
            user=request.user, pending=False).aggregate(Sum('amount'))
        total_actual_deposit = actual_deposit['amount__sum']
        
        # total pending deposit and withdrawal
        deposit_pending = deposit.filter(
            user=request.user, pending=True).aggregate(Sum('amount'))
        total_deposit_pending = deposit_pending['amount__sum']
        
        # total rejected deposit and withdraw
        deposit_rejected = deposit.filter(
            user=request.user, rejected=True).aggregate(Sum('amount'))
        total_deposit_rejected = deposit_rejected['amount__sum']
        last_deposit = deposit_history.last().amount
        
        #convert all none to 0.00
        if total_actual_deposit is None:
            total_actual_deposit = 0.00
        
        if total_deposit_pending is None:
            total_deposit_pending = 0.00
        
        if total_deposit_rejected is None:
            total_deposit_rejected = 0.00
            
    else:
        total_actual_deposit = 0.00
        total_deposit = 0.00
        total_deposit_rejected = 0.00
        total_deposit_pending = 0.00
        deposit_history = 0.00
        last_deposit = 0.00



    context = {'title': 'Deposit', 'deposits': True, 'data': deposit_history, 'total_actual_deposit': total_actual_deposit,
               'total_pending': total_deposit_pending, 'total_rejected': total_deposit_rejected,"total_deposit":total_deposit,
                "last_deposit":last_deposit,"site_name":site_name
               }
    return render(request, 'deposit/deposits.html', context)


@login_required
def addDeposit(request):
    investment_minimum = 10
    investment_maximum = 10000000000
    usdt_eth = ''
    usdt_trc = ''
    site_name = settings.SITE_NAME
    
    wallet = Wallet.objects.all()


    user_wallet = wallet.get(name='main')
    addresses = {'usdt_eth': user_wallet.usdt_ecr,'usdt_trc': user_wallet.usdt_trc}
    usdt_eth = addresses['usdt_eth']
    usdt_trc = addresses['usdt_trc']

    messages.info(request, 'Wallet generated on main-net')


    
    # Deposit form
    form = DepositForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            amount = float(form['amount'].value())
            if amount < investment_minimum-0.01 or amount > investment_maximum:
                messages.error(
                    request, f'Amount below minimum amount of ${investment_minimum} or above ${investment_maximum}')
            else:
                deposits = form.save(commit=False)
                deposits.wallet = addresses
                deposits.user = request.user
                deposits.save()
                messages.success(request, 'Deposit successful and pending')
                deposit_id=deposits.id
                print(deposit_id)
                return redirect('confirm_deposits', deposit_id=deposits.id)
        else:
            messages.error(request, 'Invalid deposit')
            
    context = {'title': 'Add Deposit', 'form': form, 'minimum':investment_minimum, "site_name":site_name, 'usdt_eth': usdt_eth, 'usdt_trc':usdt_trc}
    return render(request, 'deposit/deposit_form.html', context)

@login_required
def confirmDeposit(request, deposit_id):
    site_name = settings.SITE_NAME
    deposit = Deposit.objects.all()
    
    #get the amount from the last saved form
    recent_deposit = deposit.get(user=request.user, id=deposit_id)
    form = TransactionID(instance=recent_deposit)
    
    if request.method == 'POST':
            confirmation = TransactionID(
                request.POST or None, instance=recent_deposit)
            if confirmation.is_valid():
                confirmation.save()
                messages.success(request, 'Deposit successfully awaiting confirmation')
                return redirect(to='/deposits')
            else:
                messages.error(request, 'Deposit Not Valid')
        
    context = {'title':'Confirm Deposit', "site_name":site_name, 'recent_deposit':recent_deposit, "deposit_id":deposit_id, 'form':form}
    return render(request, 'deposit/confirm_deposit.html', context)

@login_required
def cancelTransaction(request, deposit_id):
    deposit = Deposit.objects.all()
    #get the amount from the last saved form
    recent_deposit = deposit.get(user=request.user, id=deposit_id)
    recent_deposit.rejected = True
    recent_deposit.pending = False
    recent_deposit.save()
    return redirect(to='/deposits')

@login_required
def depositDetails(request, deposit_id):
    site_name = settings.SITE_NAME
    
    deposits = Deposit.objects.all()
    deposit_details = deposits.filter(user=request.user, id=deposit_id)
    
    
    context={'title':'Deposit Details', "site_name":site_name, 'details':deposit_details}
    return render(request, 'deposit/deposit_details.html', context)
    