from django.urls import path
from .views import NewsMainPageView, NewsDetailView


urlpatterns = [
    path("", NewsMainPageView.as_view(), name="news_page"),
    path("<int:pk>/<str:my_slug>", NewsDetailView.as_view() , name="news_detail_page")
]
