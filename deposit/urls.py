from django.urls import path
from deposit import views

urlpatterns = [
    path('deposits', views.deposit_transaction, name='deposits'),
    path('add_deposit', views.addDeposit, name='add_deposit'),
    path('deposit_details/<int:deposit_id>/', views.depositDetails, name='deposit_details'),
    path('confirm_deposits/<int:deposit_id>/', views.confirmDeposit, name='confirm_deposits'),
    path('cancel_deposits/<int:deposit_id>/', views.cancelTransaction, name='cancel_deposits'),
]
