from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include

from . import views

urlpatterns = [
    path("<int:pk>/", views.UserProfileApiView.as_view(), name="profile"),
    path('', include("dj_rest_auth.urls")),
    path('registration/', include("dj_rest_auth.registration.urls")),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    ]


"""path('facebook-login/', views.FacebookLogin.as_view(), name='fb-login'),
path('google-login/', views.GoogleLogin.as_view(), name='google-login'),"""
