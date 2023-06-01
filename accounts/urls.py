from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    #path('', include('allauth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('account-confirm-email/<str:key>/', VerifyEmailView.as_view(), name='account_confirm_email'),
]
