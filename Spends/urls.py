from django.urls import path
from . import views


urlpatterns = [
    path('account/register', views.account_register, name="account_register"),
    path('account/verify/<str:random_string>', views.verify_account, name='verify_account'),
    path('account/login', views.login_page, name="login_page"),
    path('', views.index_page, name="home_page"),
    path('add_spend', views.add_spend, name="add_spend"),
    path("add_income", views.add_income, name="add_income")
]