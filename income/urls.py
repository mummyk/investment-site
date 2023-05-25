from django.urls import path
from income import views


urlpatterns = [
    path('income',views.income, name= 'income'),  
]