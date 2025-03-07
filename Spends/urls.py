from django.urls import path
from . import views


urlpatterns = [
    path('api/submit/spend', views.api_submit_spend, name="api_submit_spend"),
    path('api/submit/income', views.api_submit_income, name="api_submit_income"),
    path('api/general-stat', views.general_stats, name="api_general_stats"),
    path('account/register', views.account_register, name="account_register"),
    path('account/verify/<str:random_string>', views.verify_account, name='verify_account'),
]