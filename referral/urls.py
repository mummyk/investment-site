from django.urls import path
from .views import ref_dashboard, ref_view
from .views import ref_view

urlpatterns = [
    path('ref_dashboard/', ref_dashboard, name='ref_dashboard'),
    path('ref_view/', ref_view, name='ref_view'),
    path('referrals/<str:ref_code>', ref_view, name='ref_view'),
]
