from django.urls import path
from general import views


urlpatterns = [
    path('dashboard',views.dashboard, name= 'dashboard'),
    path('transaction',views.transactions, name= 'transactions'),   
]