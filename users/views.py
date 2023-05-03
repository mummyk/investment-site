from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress
from django.conf import settings
from .models import UserInfoModel
from referral.models import ReferralModel
from .forms import ClientInfoForm
from django_countries import countries
from django.db.models import Count
# Create your views here.

# The client profile
COUNTRY_DICT = dict(countries)

@login_required
def profiles(request):
    referral_code = ''
    verified: bool = False
    try:
        referral_code = ReferralModel.objects.all()
        referral_code = referral_code.get(user=request.user).code
        referral_code = f'{settings.ALLOWED_HOSTS[0]}/referrals/{referral_code}'

        # get email verified
        if EmailAddress.objects.filter(user=request.user, verified=True).exists():
            verified = True
    except:
        messages.info(request, 'You have no referral code')
    profile = UserInfoModel.objects.filter(user=request.user)
    

    qs = profile.values('country').annotate(
        number = Count('pk')
    ).order_by('country')

    result = {
        COUNTRY_DICT[q['country']]
        for q in qs
    }
    context = {"result":result}
    if profile.exists():
        context = {'title': 'Profile', 'profile': profile,
                   'referral_code': referral_code, 'verified': verified, "result":result}
    else:
        return redirect('create_profile')

    return render(request, 'users/view_profile.html', context)


@login_required
def create_profile(request):
    profile_form = ClientInfoForm(
        request.POST or None)
    # profile_form = ClientInfoForm(
    # request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile creation successful')
            return redirect(to='/profile')
        else:
            messages.error(request, 'Profile creation unsuccessful')
    else:
        profile_form = ClientInfoForm(
            request.POST or None, request.FILES or None)

    context = {'title': 'Create Profile', 'form': profile_form,
               'prof': profiles}
    return render(request, 'users/create_profile.html', context)


@ login_required
def edit(request):
    if UserInfoModel.objects.filter(user=request.user).exists():
        if request.method == 'POST':
            profile_form = ClientInfoForm(
                request.POST, request.FILES, instance=request.user.profile)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(
                    request, 'Your profile is updated successfully')
                return redirect(to='/profiles')
        profile = UserInfoModel.objects.get(user=request.user)
        profile_form = ClientInfoForm(instance=profile)

        context = {'title': 'Edit', 'form': profile_form,
                   'prof': profiles}
    else:
        return redirect('/create_profile')
    return render(request, 'users/edit_profile.html', context)
