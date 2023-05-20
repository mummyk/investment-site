from django.urls import path
from withdraw import views

urlpatterns = [
    path('withdraws', views.withdraw_transaction, name='withdraws'),
]
