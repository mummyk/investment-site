from django.shortcuts import render, redirect
from yahoofinancials import YahooFinancials as yf
from django.contrib.auth.decorators import login_required
from referral.models import ReferralModel
from .models import Wallet, Deposit
from .forms import DepositForm
from django.db.models import Sum
from django.contrib import messages
import urllib.request
from django.conf import settings

# Create your views here.
@login_required
def deposit_transaction(request):
    btcRate = 0
    ethRate = 0
    investment_minimum = 1000
    investment_maximum = 10000000000
    btc = ''
    eth = ''
    usdt = ''
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
        
        # total pending depoist and withdrawal
        deposit_pending = deposit.filter(
            user=request.user, pending=True)
        total_deposit_pending = deposit_pending['amount__sum']
        
        # total rejected deposit and withdraw
        deposit_rejected = deposit.filter(
            user=request.user, rejected=True)
        total_deposit_rejected = deposit_rejected['amount__sum']

        # aggregate for all pending, rejected and actual
        # pending
        deposit_pending_arg = total_deposit_pending.aggregate(
            Sum('amount'))
        total_deposit_pending_arg = deposit_pending_arg['amount__sum']

        # rejected
        deposit_rejected_arg = total_deposit_rejected.aggregate(
            Sum('amount'))
        total_deposit_rejected_arg = deposit_rejected_arg['amount__sum']
        
        last_deposit = deposit_history.last()
    else:
        total_actual_deposit = 0.00
        total_deposit = 0.00
        total_deposit_rejected = 0.00
        total_deposit_pending = 0.00
        total_deposit_rejected_arg = 0.00
        total_deposit_pending_arg = 0.00
        deposit_history = 0.00
        last_deposit = 0.00

    if connect():
        try:
            cryptocurrencies = ['BTC-USD', 'ETH-USD']
            crypto = yf(cryptocurrencies)
            yc = crypto.get_current_price()
            btcRate = yc['BTC-USD']+(yc['BTC-USD']*0.01)
            ethRate = yc['ETH-USD']+(yc['ETH-USD']*0.1)
            
        except:
            messages.error(request, 'You are not online')
    else:
        messages.error(request, 'You are offline')

    wallet = Wallet.objects.all()

    if ReferralModel.objects.all().exists:
        ref = ReferralModel.objects.all()
        if ref.filter(user=request.user).exists():
            ref_user = ref.get(user=request.user)
            if wallet.filter(name=ref_user.referred).exists():
                user_wallet = wallet.get(name=ref_user.referred)
            else:
                user_wallet = wallet.get(name='main')
            addresses = {'bitcoin': user_wallet.bitcoin,
                         'etherium': user_wallet.etherium,
                         'usdt': user_wallet.usdt}
            btc = addresses['bitcoin']
            eth = addresses['etherium']
            usdt = addresses['usdt']
        else:
            user_wallet = wallet.get(name='main')
            addresses = {'bitcoin': user_wallet.bitcoin,
                         'etherium': user_wallet.etherium,
                         'usdt': user_wallet.usdt}
            btc = addresses['bitcoin']
            eth = addresses['etherium']
            usdt = addresses['usdt']

        messages.info(request, 'Wallet generated on main-net')

    else:

        messages.error(request, 'No wallet available at the moment')

    form = DepositForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            amount = float(form['amount'].value())
            if amount < investment_minimum-0.01 or amount > investment_maximum:
                messages.error(
                    request, f'Amount below minimum amount of {investment_minimum} or above {investment_maximum}')
            else:
                deposits = form.save(commit=False)
                deposits.wallet = addresses
                deposits.user = request.user
                deposits.save()
                messages.success(request, 'Deposit successful and pending')
                return redirect(to='/deposits')
        else:
            messages.error(request, 'Invalid deposit')

    context = {'title': 'Deposit', 'deposits': True, 'data': deposit_history, 'form': form, 'total_actual_deposit': total_actual_deposit,
               'total_pending': total_deposit_pending_arg, 'total_rejected': total_deposit_rejected_arg,"total_deposit":total_deposit,
               'btcRate': btcRate, 'ethRate': ethRate, 'btc_address': btc, 'ethereum': eth,
               'usdt_address': usdt, "last_deposit":last_deposit,"site_name":site_name
               }
    return render(request, 'deposit/deposits.html', context)




def connect():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False