from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.account.decorators import verified_email_required



# Create your views here.
@login_required
@verified_email_required
def dashboard(request):
   context = {"title":"Dashboard"}
   return render(request, "general/dashboard/dashboard.html", context)


def termsAndCondition(request):
   context = {"title":'Terms & Conditions'}
   return render(request, "general/t&c.html")