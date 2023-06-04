from django.shortcuts import render, redirect
from .models import ReferralModel, Ref_withdrawal, Ref_deposit, Referral_percentage
from deposit.models import Deposit
from withdraw.models import Withdrawal
from .forms import ReferralForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# # Create your views here.
my_recs = []

@login_required
def ref_dashboard(request):
    site_name = settings.SITE_NAME
    total_ref = []
    amount = 0
    person = ''
    form = ReferralForm(request.POST or None)
    if Deposit.objects.all().exists():
        deposit = Deposit.objects.all()
        ref = ReferralModel.objects.all()
        # to get the users who referred them
        for r in ref:
            if request.user == r.referred:
                my_recs.append(r.user)
        total_ref = len(my_recs)

    # get the deposit of the referred user
        ref_deposits = ref_deposit(deposit, my_recs)
        person = ref_deposits['person']
        amount = ref_deposits['amount']
    # get the available ref balance
        ref_withdraws = ref_withdraw(Withdrawal, my_recs)
        ref_bonus_withdraw = ref_bonus_withdraws(request)
        total_ref_balance = (amount+ref_withdraws)-ref_bonus_withdraw

    # Verify the amount to withdraw withe the available balance
        
        if request.method == 'POST':
            if form.is_valid:
                amount = float(form['amount'].value())
                if amount >= total_ref_balance:
                    form.add_error(
                        'amount', f'Amount should not be more that {total_ref_balance}')
                else:
                    ref_form = form.save(commit=False)
                    ref_form.user = request.user
                    ref_form.save()

    else:
        messages.info(request,  'No Referral bonus yet')

    context = context = {'title': 'Referral Dashboard',
                         'my_record': my_recs,  'person': person,
                         'Total_user_ref': amount, 'total_ref': total_ref, 'form': form, 'site_name':site_name
                         }
    return render(request, 'referrals/ref_dashboard.html', context)


@login_required
def ref_view(request, *args, **kwargs):
    site_name = settings.SITE_NAME
    code = str(kwargs.get('ref_code'))
    try:
        if ReferralModel.objects.all().exists():
            referrals = ReferralModel.objects.all()
            referral = referrals.get(code=code)
            request.session['ref_profile'] = referral.user.id
            redirect('/accounts/signup')
        else:
            messages.info(request, 'You do not have a referral code')
    except:
        pass

    context = {'title': 'Referrals', 'site_name':site_name}
    return render(request, 'referrals/ref_views.html', context)


# allowing referral withdraw
def ref_withdraw(db, val):
    available_ref_balance = 0.00
    amount = 0.00
    for i in val:
        if db.objects.all().exists():
            db_val = db.objects.all()
            if db_val.filter(user=i):
                j = db_val.filter(user=i)
                if j.filter(pending=False):
                    person = i
                    amount = j.filter(user=i, pending=False).aggregate(
                        Sum('amount'))
                    amount = amount['amount__sum']
            # All confirmed withdraw
            available_ref_balance = amount * 0.05
            # get all referred bonus amount

    return available_ref_balance


def ref_bonus_withdraws(request):
    if Ref_bonus_withdrawal.objects.all().exists():
        ref_bonus_withdraw = Ref_bonus_withdrawal.objects.all()
        ref_bonus_withdraw = ref_bonus_withdraw.filter(
            user=request.user, withdrawal_confirmation=False).aggregate(
            Sum('amount'))
        ref_bonus_withdraw = ref_bonus_withdraw['amount__sum']
    return ref_bonus_withdraw


# referral balance
def ref_deposit(db, val):
    ref_percentge = Referral_percentage.objects.get(name="deposit")
    for i in val:
        if db.filter(user=i):
            j = db.filter(user=i)
            if j.get(pending=False, rejected=False):
                person = i
                amount = sum(j.filter(
                    user=i).values_list('amount', flat=True))
                # 5% for the deposit
                amount = amount * ref_percentge.percentage
                amount = round(amount, 2)
    return {'amount': amount, 'person': person}


# referral number of downlink
def downlink(number_of_downlink=3):
    if ReferralModel.object.all().exists():
        ref = ReferralModel.objects.all()
        ref_downlink = number_of_downlink
        return ref_downlink

# Save for every deposit of the referred
@receiver(post_save, sender=Deposit)
def ref_deposit_save(sender, instance, created, *args, **kwargs):
    if created:
        if ReferralModel.objects.all().exists():
            referral = ReferralModel.objects.all()
            deposits = Deposit.objects.all()
                        
            # get the deposit of the referred user
            ref_deposits = ref_deposit(deposits, my_recs)
            person = ref_deposits['person']
            amount = ref_deposits['amount']
            
            refer_by = referral.filter(user=person)
            referred_by = refer_by.referred_by
            
            # Save the referred user and the amount
            deposited_by_ref = Ref_deposit.objects.create(user=referred_by, referred_person=person, amount=amount)
        
# Save for every withdraw of the referred
@receiver(post_save, sender=Withdrawal)
def ref_withdraw_save(sender, instance, created, *args, **kwargs):
    if created:
        ReferralModel.objects.create(user=instance)
        

# #TODO remove this is an example
# @login_required
# def ref_view(request, *args, **kwargs):
#    code = str(kwargs.get('ref_code'))
     
#    print(code)
#    redirect('/accounts/signup')