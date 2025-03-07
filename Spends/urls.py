from django.urls import path
from . import views


urlpatterns = [
    path('submit/spend', views.submit_spend, name="submit_spend"),
    path('submit/income', views.submit_income, name="submit_income"),
    path('account/register', views.account_register, name="account_register"),
    path('account/verify/<str:random_string>', views.verify_account, name='verify_account')
]