from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterUserApiView.as_view(), name="register"),
]
