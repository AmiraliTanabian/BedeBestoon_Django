import datetime
from bs4 import BeautifulSoup
import requests
from . import chart_handel
from secrets import choice
from string import digits, punctuation, ascii_letters

from django.shortcuts import render
from .models import Spend, Income
from django.utils import timezone
from .forms import addSpend, addIncome, editIncome
from django.db.models.aggregates import Sum
from django.urls import reverse_lazy
from django.db.models import Avg, Max, Min
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


def random_str(length):
    all_letters = digits + punctuation + ascii_letters
    all_letters = all_letters.replace(r'/', '')
    all_letters = all_letters.replace('\\', '')
    result = ''.join(choice(all_letters) for _ in range(length))
    return result
def index_page(request):
    user = request.user
    if request.user.is_authenticated:
        try:
            spend_aggregate = Spend.objects.filter(user=user).aggregate(Max('price'), Min('price'),Avg('price'))
            min_spend = int(spend_aggregate['price__min'])
            max_spend = int(spend_aggregate['price__max'])
            avg_spend = int(spend_aggregate['price__avg'])

        except TypeError :
            min_spend = max_spend = avg_spend = "شما هنور خرجی ندارید:)"

        try:
            income_aggregate = Income.objects.filter(user=user).aggregate(Max('price'), Min('price'), Avg('price'))
            min_income = int(income_aggregate['price__min'])
            max_income = int(income_aggregate['price__max'])
            avg_income = int(income_aggregate['price__avg'])

        # Db is empty and can convert None type to int
        except TypeError:
            min_income = max_income = avg_income = "شما هنوز درآمدی ندارید:)"

        try:
            context = {
                'username': user.username,
                'max_spend': f'{max_spend:,d}',
                'min_spend': f'{min_spend: ,d}',
                'avg_spend': f'{avg_spend: ,d}',
                'max_income': f'{max_income: ,d}',
                'min_income': f'{min_income: ,d}',
                'avg_income': f'{avg_income: ,d}'
            }


        # The database is empty and cannot separate the 3 digit None values.
        except ValueError:
            context = {
                'username': user.username,
                'max_spend': max_spend,
                'min_spend': min_spend,
                'avg_spend': avg_spend,
                'max_income': max_income,
                'min_income': min_income,
                'avg_income': avg_income,
            }



        # For filter box handel
        if request.method != 'POST':
            return render(request, 'Spends/dashboard.html', context)


        else:
            spend_time_filter = request.POST.get('spend_time_filter')
            income_time_filter = request.POST.get('income_time_filter')

            spends = None
            if spend_time_filter == 'all':
                spends = Spend.objects.filter(user=request.user)

            elif spend_time_filter == 'last_ten':
                spends = Spend.objects.filter(user=request.user).order_by('time')[:10]

            elif spend_time_filter == 'week':
                now_date = timezone.now().isocalendar()
                now_week = now_date[1]
                now_year = now_date[0]
                spends = Spend.objects.filter(user=request.user, time__year=now_year, time__week=now_week)

            elif spend_time_filter == 'month':
                now_year = timezone.now().year
                now_month = timezone.now().month
                spends = Spend.objects.filter(user=request.user, time__year=now_year, time__month=now_month)

            elif spend_time_filter == 'year':
                now_year = timezone.now().year
                spends = Spend.objects.filter(user=request.user, time__year = now_year)

            else:
                messages.error(request, "لطفا یک زمان را برای نمایش هزینه ها انتخاب کنید")
                return render(request, 'Spends/dashboard.html', context)

            context['spends'] = spends

            incomes = None
            if income_time_filter == "all":
                incomes = Income.objects.filter(user=request.user)

            elif income_time_filter == "last_ten":
                incomes = Income.objects.filter(user=request.user).order_by("time")[:10]

            elif income_time_filter == 'week':
                now_date = timezone.now().isocalendar()
                now_week = now_date[1]
                now_year = now_date[0]
                incomes = Income.objects.filter(user=request.user, time__year=now_year, time__week=now_week)

            elif income_time_filter == 'month':
                now_year = timezone.now().year
                now_month = timezone.now().month
                incomes = Income.objects.filter(user=request.user, time__year=now_year, time__month=now_month)

            elif income_time_filter == 'year':
                now_year = timezone.now().year
                incomes = Income.objects.filter(user=request.user, time__year=now_year)

            else:
                messages.error(request, "لطفا یک زمان را برای نمایش درآمد ها انتخاب کنید")
                return render(request, 'Spends/dashboard.html', context)

            context["incomes"] = incomes

            context['income_filter'] = income_time_filter
            context["spend_filter"] = spend_time_filter

            return render(request, 'Spends/dashboard.html', context)


    else:
        return  render(request, "Spends/home_page.html", {"login":False})

class AddSpendView(LoginRequiredMixin,View):
    login_url = reverse_lazy("login_page")
    def get(self, request):
        add_spend_obj = addSpend()
        context = {'form_obj':add_spend_obj}
        return render(request, 'Spends/add_spend.html', context)

    def post(self, request):
        add_spend_obj = addSpend(data=request.POST)

        note = request.POST['note']
        title = request.POST['title']
        price = request.POST['price']
        is_now = 'is_now' in request.POST

        if is_now:
            datetime_obj = timezone.now()

        else:
            # date[0] date and date[1] time
            date_result = request.POST['datetime'].split('T')
            date = date_result[0].split('-')
            time = date_result[1].split(':')

            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            hour = int(time[0])
            minute = int(time[1])
            datetime_obj = datetime.datetime(year, month, day, hour, minute)

        Spend.objects.create(user=request.user, title=title, time=datetime_obj, price=price, note=note)
        context = {'form_obj': add_spend_obj, 'status': True}
        return render(request, 'Spends/add_spend.html', context)

class AddIncomeView(LoginRequiredMixin,View):
    login_url = reverse_lazy("login_page")
    def get(self, request):
        add_income_obj = addIncome()
        context = {'form_obj':add_income_obj}
        return render(request, 'Spends/add_income.html', context)

    def post(self, request):
        add_income_obj = addIncome(data=request.POST)

        note = request.POST['note']
        title = request.POST['title']
        price = request.POST['price']
        is_now = 'is_now' in request.POST

        if is_now:
            datetime_obj = timezone.now()

        else:
            # date[0] date and date[1] time
            date_result = request.POST['datetime'].split('T')
            date = date_result[0].split('-')
            time = date_result[1].split(':')

            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            hour = int(time[0])
            minute = int(time[1])
            datetime_obj = datetime.datetime(year, month, day, hour, minute)

        Income.objects.create(user=request.user, title=title, time=datetime_obj, price=price, note=note)
        context = {'form_obj': add_income_obj, 'status': True}
        return render(request, 'Spends/add_income.html', context)


def header(request):
    context = {"is_login":request.user.is_authenticated}
    return render(request, "Spends/header_component.html", context)

class HomePageView(TemplateView):
    template_name = "Spends/home_page.html"
class IncomeDetailView(LoginRequiredMixin, DetailView):
    template_name = "Spends/income_details.html"
    model = Income
    context_object_name = "income"
    login_url = reverse_lazy("login_page")

class SpendDetailView(LoginRequiredMixin, DetailView):
    template_name = "Spends/spend_detail.html"
    model = Spend
    context_object_name = "spend"
    login_url = reverse_lazy("login_page")
class DeleteIncomeView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")
    def get(self, request, id):
        income_name = get_object_or_404(Income, user=request.user, id=id)
        return render(request, "Spends/delete_income_verify.html", {'name': income_name.title, 'id': id})


    def post(self, request, id):
        if "ok" in request.POST:
            income_object = Income.objects.get(user=request.user, id=id)
            name = income_object.title
            income_object.delete()
            return render(request, "Spends/delete_income_success.html", {'name':name})

class DeleteSpendView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")

    def get(self, request, id):
        spend_name = get_object_or_404(Spend, user=request.user, id=id)
        return render(request, "Spends/delete_spend_verify.html", {'name': spend_name.title, 'id': id})

    def post(self, request, id):
        if "ok" in request.POST:
            spend_object = Spend.objects.get(user=request.user, id=id)
            name = spend_object.title
            spend_object.delete()
            return render(request, "Spends/delete_spend_success.html", {'name': name})

class EditIncomeView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")
    def dispatch(self, request, *args, **kwargs):
        # Set init value
        id = kwargs["id"]
        income = get_object_or_404(Income, user=request.user, id=id)
        self.title = income.title
        self.price = income.price
        self.note = income.note
        self.time = income.time
        self.year = self.time.year
        self.month = self.time.month
        self.day = self.time.day
        self.minute = self.time.minute
        self.hour = self.time.hour

        # Convert to html format : For example 7 --> 07
        if len(str(self.hour)) == 1:
            self.hour = "0" + str(self.hour)

        # For example 1 --> 01
        if len(str(self.minute)) == 1:
            self.minute = "0" + str(self.minute)

        if len(str(self.month)) == 1:
            self.month = "0" + str(self.month)

        if len(str(self.day)) == 1:
            self.day = "0" + str(self.day)

        # DATATIME html format example: 2025-03-11T07:37
        self.html_time_format = f"{self.year}-{self.month}-{self.day}T{self.hour}:{self.minute}"

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        form_obj = editIncome(initial={"title":self.title, "price":self.price, "note":self.note})
        income = get_object_or_404(Income, user=request.user, id=id)
        return render(request, "Spends/edit_income.html",
                      {"form_obj":form_obj, "income":income, 'date':self.html_time_format})


    def post(self, request, id):
        form_obj = editIncome(data=request.POST)

        income = get_object_or_404(Income, user=request.user, id=id)
        old_name = income.title
        income.title = request.POST['title']
        income.price = request.POST['price']
        income.note = request.POST['note']


        is_now = 'is_now' in request.POST.keys()

        if is_now:
            datetime_obj = timezone.now()

        else:
            # date[0] date and date[1] time
            date_result = request.POST['datetime'].split('T')
            date = date_result[0].split('-')
            time = date_result[1].split(':')

            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            hour = int(time[0])
            minute = int(time[1])
            datetime_obj = datetime.datetime(year, month, day, hour, minute)

        income.time = datetime_obj
        income.save()


        return render(request, "Spends/edit_income_success.html",
                      {'form_obj':form_obj, 'name':old_name})

def chart(request):
    is_chart_submit = 'chart_time_filter' in request.GET
    if not is_chart_submit:
        return render(request, "Spends/chart.html")

    else:
        chart_filter = request.GET['chart_time_filter']

        # User has not selected item yet
        if chart_filter == "select":
            return render(request, "Spends/chart.html", {"chart_filter":chart_filter, "has_error":True,
                                                         "error_msg":"لطفا زمان مورد نظر را انتخاب کنید."})

        # ___________________________________YEAR__________________________________
        if chart_filter == "year" :
            spends = chart_handel.year_spend_data(request)
            incomes = chart_handel.year_income_data(request)
            month_shamsi = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی',
                            'بهمن', 'اسفند']

            miladi_to_shamsi = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            spends_shamsi_date = [spends[miladi_to_shamsi.index(i + 1)] for i in range(12)]
            incomes_shamsi_date = [incomes[miladi_to_shamsi.index(i + 1)] for i in range(12)]


            return render(request, "Spends/chart.html",
                          {"spend_data":spends_shamsi_date, "income_data":incomes_shamsi_date, "label":month_shamsi,
                           'chart_filter':chart_filter})


        # ___________________________________MONTH__________________________________
        if chart_filter == "month":
            spends = chart_handel.month_spend_data(request)
            incomes = chart_handel.month_income_data(request)
            month_day = [day for day in range(1, 31)]

            return render(request, "Spends/chart.html", {"spend_data":spends, "income_data":incomes, "label":month_day,
                           'chart_filter':chart_filter})

        # __________________________________WEEK______________________________________
        if chart_filter == "week":
            spends = chart_handel.week_spend_data(request)
            incomes = chart_handel.week_income_data(request)
            week_days = ["شنبه", "یکشنه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنج شنبه", "جمعه"]

            return render(request, "Spends/chart.html", {"spend_data":spends, "income_data":incomes, "label":week_days,
                                                         'chart_filter':chart_filter})


        #_________________________________LAST TEN________________________________________
        if chart_filter == "last_ten":
            spends = chart_handel.last_ten_spend_data(request)
            incomes = chart_handel.last_ten_income_data(request)
            labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

            print(spends)
            print(incomes)
            return render(request, "Spends/chart.html", {"spend_data":spends, "income_data":incomes, "label":labels,
                                                         "chart_filter":chart_filter})

class EditSpendView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")
    def dispatch(self, request, *args, **kwargs):
        # Set init value
        id = kwargs["id"]
        spend = get_object_or_404(Spend, user=request.user, id=id)
        self.title = spend.title
        self.price = spend.price
        self.note = spend.note
        self.time = spend.time
        self.year = self.time.year
        self.month = self.time.month
        self.day = self.time.day
        self.minute = self.time.minute
        self.hour = self.time.hour

        # Convert to html format : For example 7 --> 07
        if len(str(self.hour)) == 1:
            self.hour = "0" + str(self.hour)

        # For example 1 --> 01
        if len(str(self.minute)) == 1:
            self.minute = "0" + str(self.minute)

        if len(str(self.month)) == 1:
            self.month = "0" + str(self.month)

        if len(str(self.day)) == 1:
            self.day = "0" + str(self.day)

        # DATATIME html format example: 2025-03-11T07:37
        self.html_time_format = f"{self.year}-{self.month}-{self.day}T{self.hour}:{self.minute}"

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        form_obj = editIncome(initial={"title":self.title, "price":self.price, "note":self.note})
        spend = get_object_or_404(Spend, user=request.user, id=id)
        return render(request, "Spends/edit_spends.html",
                      {"form_obj":form_obj, "spend":spend, 'date':self.html_time_format})


    def post(self, request, id):
        form_obj = editIncome(data=request.POST)

        spend = get_object_or_404(Spend, user=request.user, id=id)
        old_name = spend.title
        spend.title = request.POST['title']
        spend.price = request.POST['price']
        spend.note = request.POST['note']


        is_now = 'is_now' in request.POST

        if is_now:
            datetime_obj = timezone.now()

        else:
            # date[0] date and date[1] time
            date_result = request.POST['datetime'].split('T')
            date = date_result[0].split('-')
            time = date_result[1].split(':')

            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            hour = int(time[0])
            minute = int(time[1])
            datetime_obj = datetime.datetime(year, month, day, hour, minute)

        spend.time = datetime_obj
        spend.save()


        return render(request, "Spends/edit_spend_success.html",
                      {'form_obj':form_obj, 'name':old_name})

def profit_or_loss(request):
    user = request.user
    now_month = timezone.now().month
    now_year = timezone.now().year
    now_day = timezone.now().day
    now_week = timezone.now().isocalendar()[1]

    user_spends = Spend.objects.filter(user=user)
    user_incomes = Income.objects.filter(user=user)


    # Year
    user_spends_year = user_spends.filter(time__year=now_year)
    user_incomes_year = user_incomes.filter(time__year=now_year)


    # Month
    user_spends_month = user_spends_year.filter(time__month=now_month)
    user_income_month = user_incomes_year.filter(time__month=now_month)


    # Week
    user_spends_week = user_spends_year.filter(time__week=now_week)
    user_incomes_week = user_incomes_year.filter(time__week=now_week)


    # Day
    user_spends_day = user_spends_month.filter(time__day=now_day)
    user_incomes_day = user_income_month.filter(time__day=now_day)

    # Calc Sum
    month_spends_sum = user_spends_month.aggregate(Sum("price"))["price__sum"]
    month_incomes_sum = user_income_month.aggregate(Sum("price"))["price__sum"]

    day_spends_sum = user_spends_day.aggregate(Sum("price"))["price__sum"]
    day_incomes_sum = user_incomes_day.aggregate(Sum("price"))["price__sum"]

    year_spends_sum = user_spends_year.aggregate(Sum("price"))["price__sum"]
    year_incomes_sum = user_incomes_year.aggregate(Sum("price"))["price__sum"]

    week_spends_sum = user_spends_week.aggregate(Sum("price"))["price__sum"]
    week_incomes_sum = user_incomes_week.aggregate(Sum("price"))["price__sum"]

    # Calc difference to detect profits or loss
    if month_incomes_sum is None or month_spends_sum is None:
        month_result = None
    else:
        month_result =  month_incomes_sum - month_spends_sum

    if day_incomes_sum is None or day_spends_sum is None:
        day_result = None
    else:
        day_result = day_incomes_sum - day_spends_sum

    if year_incomes_sum is None or year_spends_sum is None:
        year_result = None
    else:
        year_result = year_incomes_sum - year_spends_sum


    if week_incomes_sum is None or week_spends_sum is None:
        week_result = None
    else:
        week_result = week_incomes_sum - year_spends_sum


    context = {
        "year":year_result,
        "day":day_result,
        "week":week_result,
        "month":month_result
    }

    return render(request, "Spends/profit_or_loss.html", context)

def currency_coin(request):
    response = requests.get("https://www.tgju.org/currency")
    parser = BeautifulSoup(response.text, "html.parser")

    if response.status_code == 200 :
        dollar = parser.select_one('table.data-table tr[data-market-nameslug="price_dollar_rl"] td.nf').contents[0]
        uro = parser.select_one('table.data-table tr[data-market-nameslug="price_eur"] td.nf').contents[0]
        coin = parser.select_one('li#l-sekee span.info-price').contents[0]
        gold = parser.select_one('li#l-geram18 span.info-price').contents[0]

        context = {
            "dollar":dollar,
            "uro":uro,
            "coin":coin,
            "gold":gold,
           }

    else:
        context = {
            "dollar": "مشکلی در برقراری ارتباط پیش آمده!",
            "uro": "مشکلی در برقراری ارتباط پیش آمده!",
            "coin": "مشکلی در برقراری ارتباط پیش آمده!",
            "gold": "مشکلی در برقراری ارتباط پیش آمده!",
        }

    return render(request, "Spends/currency_coin.html", context)