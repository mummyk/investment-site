from django.urls import path
from deposit import views

urlpatterns = [
    path('deposits', views.deposit_transaction, name='deposits'),
]
