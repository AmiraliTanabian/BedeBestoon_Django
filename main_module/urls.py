from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_page, name="home_page"),
    path('add_spend', views.AddSpendView.as_view() , name="add_spend"),
    path("add_income", views.AddIncomeView.as_view() , name="add_income"),
    path('home', views.HomePageView.as_view() , name="home"),
    path("spend/<int:pk>", views.SpendDetailView.as_view(), name="spend_detail"),
    path("income/<int:pk>", views.IncomeDetailView.as_view(), name="income_detail"),
    path("delete-income/<int:id>", views.DeleteIncomeView.as_view() , name="delete_income"),
    path("edit-income/<int:id>", views.EditIncomeView.as_view() , name="edit_income"),
    path("edit-spend/<int:id>", views.EditSpendView.as_view(), name="edit_spend"),
    path("delete-spend/<int:id>", views.DeleteSpendView.as_view(), name="delete_spend"),
]