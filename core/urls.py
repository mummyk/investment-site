"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Third party apps
    path('__debug__/', include('debug_toolbar.urls')),
    path('accounts/', include('allauth.urls')),

    # My apps
    path('', include('general.urls')),
    path('', include('users.urls')),
    path('', include('referral.urls')),
    path('', include('deposit.urls')),
    path('', include('withdraw.urls')),
]


handler400 = "helper.views.handle_400_error"
handler403 = "helper.views.handle_403_error"
handler404 = "helper.views.handle_404_error"
handler500 = "helper.views.handle_500_error"
