from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from deposit.models import Deposit
from income.models import Profit, Bonus, Withdrawable
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User

# Create your views here.
@login_required
def income(request):
   site_name = settings.SITE_NAME
   last_bonus = 0.00
   total_income = 0.00
   total_bonus = 0.00
   last_profit = 0.00
   user_total_profit = 0.00
   expired_bonus = 0.00
   all_user_bonus = 0.00
   user_bonus = 0.00
   profits = 0.00
   
   if Deposit.objects.filter(user=request.user).exists():
      all_deposit = Deposit.objects.all()
      deposit = all_deposit.filter(user=request.user, pending = False, rejected = False)
      total_deposit = deposit.aggregate(Sum('amount'))
      total_deposit = total_deposit['amount__sum']
      
       # Your total profit
      if Profit.objects.all().exists():
         first_deposit = deposit.filter(
               user=request.user, pending=False).first()
         profit = Profit.objects.all()
         first_day = first_deposit.created
         profits = profit.filter(
               created__gte=first_day)
         last_profit = profit.last()
         # add the profit from the day of the first deposit
         total_profit = profit.aggregate(Sum('amount'))
         user_total_profit = total_profit['amount__sum']
         
      if Bonus.objects.all().exists():
         all_bonus = Bonus.objects.all()
         all_user_bonus = all_bonus.filter(user=request.user)
         user_bonus = all_user_bonus.filter(expired=False)
         expired_bonus = all_user_bonus.filter(expired=True)
         
         # Sum up all the bonuses
         all_user_bonus = all_user_bonus.aggregate(Sum('bonuses'))
         all_user_bonus = all_user_bonus['bonuses__sum']
         
         user_bonus = user_bonus.aggregate(Sum('bonuses'))
         user_bonus = user_bonus['bonuses__sum']
         
         expired_bonus = expired_bonus.aggregate(Sum('bonuses'))
         expired_bonus = expired_bonus['bonuses__sum']
         
   else:
      messages.info(request, 'Make a deposit to start earning') 
      
   
   context = {'title': 'Income',"site_name":site_name, 'profits':profits, 'last_profit':last_profit, 'user_total_profit':user_total_profit,'expired_bonus':expired_bonus,'user_bonus':user_bonus,'all_user_bonus':all_user_bonus}
   return render(request, "income/income.html", context)


#Edit the Withdraw able from profit
@receiver(post_save, sender=Profit)
def post_save_create_withdrawable(sender, instance, created, *args, **kwargs):
    if created:
         user = User.objects.all()
         deposit = Deposit.objects.all()
         for i in user:
            user_deposit = deposit.filter(user=i, pending=False, rejected=False).aggregate(Sum('amount'))
            user_deposit = user_deposit['amount__sum']
            if user_deposit is None:
               user_deposit = 0.00
            profit = (instance.amount/100)*user_deposit
            Withdrawable.objects.create(user=i,profit_amount=profit, profit_id=instance.id)
            
   
@receiver(post_delete, sender=Profit)
def delete_withdrawable(sender, instance, *args, **kwargs):
   user = User.objects.all()
   for i in user:
      if Withdrawable.objects.filter(user=i).exists():
         withdrawable = Withdrawable.objects.all()
         withdrawable =withdrawable.filter(profit_id=instance.id).delete()
               
            
              
            
@login_required
def depositWithdrawn(request):
   pass