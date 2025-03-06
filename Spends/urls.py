from django.urls import path
from . import views


urlpatterns = [
    path('submit/spend', views.submit_spend, name="submit_spend")
]