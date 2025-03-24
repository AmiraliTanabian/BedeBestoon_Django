from django.views.generic import DetailView, ListView
from .models import NewsModel

class NewsDetailView(DetailView):
    model = NewsModel
    template_name = "news_module/detail.html"
    context_object_name = "news"

class NewsMainPageView(ListView):
    model = NewsModel
    template_name = "news_module/list.html"
    context_object_name = "news"
    paginate_by = 5

    def get_queryset(self):
        return  NewsModel.objects.filter(is_active=True)

