from django.urls import path
from withdraw import views

urlpatterns = [
    path('withdraws', views.withdraw_transaction, name='withdraws'),
    path('add_withdraw', views.addWithdraw, name='add_withdraw'),
    path('withdraw_details/<int:withdraw_id>/', views.withdrawDetails, name='withdraw_details'),
    path('confirm_withdraws/<int:withdraw_id>/', views.confirmWithdraw, name='confirm_withdraws'),
    path('cancel_withdraws/<int:withdraw_id>/', views.cancelTransaction, name='cancel_withdraws'),

]
