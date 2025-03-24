from django.urls import path
from . import views

urlpatterns = [
    path('register', views.AccountRegisterView.as_view() , name="account_register"),
    path('verify/<str:random_string>', views.VerifyAccountView.as_view(), name='verify_account'),
    path('login', views.LoginView.as_view(), name="login_page"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("forget-password", views.ForgetPasswordView.as_view(), name="forget_password"),
    path("reset-password/<str:random_string>", views.ResetPasswordView.as_view(), name="reset_password")

]