from django.urls import path
from . import views

urlpatterns = [
    path('submit/spend', views.api_submit_spend, name="api_submit_spend"),
    path('submit/income', views.api_submit_income, name="api_submit_income"),
    path('general-stat', views.api_general_stats, name="api_general_stats"),
    path('account/login', views.api_login, name="api_login"),
]