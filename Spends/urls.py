from django.urls import path
from . import views


urlpatterns = [
    path('api/submit/spend', views.api_submit_spend, name="api_submit_spend"),
    path('api/submit/income', views.api_submit_income, name="api_submit_income"),
    path('api/general-stat', views.api_general_stats, name="api_general_stats"),
    path('api/account/login', views.api_login, name="api_login"),
    path('account/register', views.account_register, name="account_register"),
    path('account/verify/<str:random_string>', views.verify_account, name='verify_account'),
    path('account/login', views.login_page, name="login_page"),
    path('', views.index_page, name="home_page"),
    path('add_spend', views.add_spend, name="add_spend"),
    path("add_income", views.add_income, name="add_income")
]