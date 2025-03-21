import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Token, Spend, Income, TempUser
from django.utils import timezone
from .forms import registerForm, loginForm, addSpend, addIncome, editIncome
from secrets import choice
from string import digits, punctuation, ascii_letters
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.db.models import Avg, Max, Min
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import get_object_or_404
from . import chart_handel
from django.views.generic import TemplateView
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

def login_verify(func):
    def inner_verify(request, **kwargs):
        if request.user.is_authenticated:

            if 'id' in kwargs :
                return func(request, kwargs.get("id"))

            else:
                return func(request)
        else:
            return render(request, "Spends/unauthorized.html")
    return inner_verify

def random_str(length):
    all_letters = digits + punctuation + ascii_letters
    all_letters = all_letters.replace(r'/', '')
    all_letters = all_letters.replace('\\', '')
    result = ''.join(choice(all_letters) for _ in range(length))
    return result

class AccountRegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "Spends/login_register_limit.html")

        else:
            form_object = registerForm()
            return render(request, 'Spends/register.html',
                          {'status':False , 'form_object':form_object})


    def post(self, request):
        form_object = registerForm(data=request.POST)

        if form_object.is_valid():
            form_object = registerForm(data=request.POST)
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']


            #TODO; check the user dont on temp users
            #TODO; check ip
            #TODO; remove TempUser
            random_string = random_str(50)

            # Add temp info on table
            TempUser.objects.create(username=username, password=make_password(password),
                                    date=timezone.now() , email=email, random_str=random_string)
            # Send verify email
            verification_url = settings.SITE_URL +  reverse_lazy('verify_account', args=[random_string])
            email_subject = 'تایید حساب کاربری'
            email_html_content = render_to_string('Spends/email_sender.html',
                                                    {'verification_url':verification_url})
            email_from = 'atanabain@gmail.com'

            mail = EmailMessage(email_subject, email_html_content, email_from, [email])
            mail.content_subtype = 'html'
            mail.send()


            return render(request, 'Spends/register.html',
                        {'status':'OK', 'form_object':form_object})

        else:
            return render(request, 'Spends/register.html',
                {'status':False , 'form_object':form_object})

class VerifyAccountView(View):
    def get(self, request, random_string):
        temp_object = TempUser.objects.filter(random_str=random_string)

        if not temp_object.exists():
            print("Salam")
            return render(request, 'Spends/verify_account.html', {'status': 'NotFound'})


        elif timezone.now().timestamp() - temp_object[0].date.timestamp() > 12 * 3600:
            return render(request, 'Spends/verify_account.html', {'status': 'Expired'})


        else:
            temp_object = temp_object.first()
            username = temp_object.username
            user_object = User(username=temp_object.username, password=temp_object.password, email=temp_object.email)
            user_object.save()
            this_token = Token(user=user_object, token=random_str(50))
            this_token.save()
            temp_object.delete()
            return render(request, 'Spends/verify_account.html', {'status': 'Ok', 'username': username,
                                                                  'token': this_token.token})

class LoginView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form_obj = loginForm()
            return render(request, 'Spends/login.html', {'form_obj': form_obj})

        else:
            return render(request, "Spends/login_register_limit.html")

    def post(self, request):
        form_obj = loginForm(data=request.POST)

        if form_obj.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user :
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد اکانت خود شدید!\nمیتوانید از امکانات سرویس استفاده کنید')
                return  HttpResponseRedirect(reverse('home_page'))

            else:
                return render(request, 'Spends/login.html', {'status':'username or password incorrect',
                                                             'form_obj':form_obj})

        else:
            return render(request, 'Spends/login.html', {'form_obj': form_obj})


def db_not_empty(func):
    def wrapper(request):
        if request.user.is_authenticated:

            try:
                user = request.user
                income_count = Income.objects.filter(user=user).count()
                spend_count = Spend.objects.filter(user=user).count()
                if spend_count and income_count:
                    return func(request)
                else:
                    return render(request, "Spends/dont_have_spend_income.html")

            except Exception as Error:
                print(Error)

        else:
            return func(request)

    return wrapper

@db_not_empty
def index_page(request):
    if request.user.is_authenticated:
        user = request.user
        spend_aggregate = Spend.objects.filter(user=user).aggregate(Max('price'), Min('price'),
                                                                    Avg('price'))
        min_spend = int(spend_aggregate['price__min'])
        max_spend = int(spend_aggregate['price__max'])
        avg_spend = int(spend_aggregate['price__avg'])
        income_aggregate = Income.objects.filter(user=user).aggregate(Max('price'), Min('price'),
                                                                      Avg('price'))
        min_income = int(income_aggregate['price__min'])
        max_income = int(income_aggregate['price__max'])
        avg_income = int(income_aggregate['price__avg'])
        context = {
            'username': user.username,
            'max_spend': f'{max_spend:,d}',
            'min_spend': f'{min_spend: ,d}',
            'avg_spend': f'{avg_spend: ,d}',
            'max_income': f'{max_income: ,d}',
            'min_income': f'{min_income: ,d}',
            'avg_income': f'{avg_income: ,d}'
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
class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            context = {"username": username}
            return render(request, "Spends/logout.html", context)

        else:
            return render(request, "Spends/logout_without_login.html")
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


@login_verify
def edit_income(request, id):
    # Set init value
    income = get_object_or_404(Income, user=request.user, id=id)
    title = income.title
    price = income.price
    note = income.note
    time = income.time
    year = time.year
    month = time.month
    day = time.day
    minute = time.minute
    hour = time.hour

    # Convert to html format : For example 7 --> 07
    if len(str(hour)) == 1:
        hour = "0" + str(hour)

    # For example 1 --> 01
    if len(str(minute)) == 1:
        minute = "0" + str(minute)

    if len(str(month)) == 1:
        month = "0" + str(month)

    if len(str(day)) == 1:
        day = "0" + str(day)


    # DATATIME html format example: 2025-03-11T07:37
    html_time_format = f"{year}-{month}-{day}T{hour}:{minute}"


        # End convert the datetime to html format



    if request.method != "POST":
        form_obj = editIncome(initial={"title":title, "price":price, "note":note})



        income = get_object_or_404(Income, user=request.user, id=id)
        return render(request, "Spends/edit_income.html",
                      {"form_obj":form_obj, "income":income, 'date':html_time_format})

    else:
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

@login_verify
def edit_spend(request, id):
    # pay attention : we don't create specific form for spend edit because the income edit form is simular
    # Set init value
    spend = get_object_or_404(Spend, user=request.user, id=id)
    title = spend.title
    price = spend.price
    note = spend.note
    time = spend.time
    year = time.year
    month = time.month
    day = time.day
    minute = time.minute
    hour = time.hour

    # Convert to html format : For example 7 --> 07
    if len(str(hour)) == 1:
        hour = "0" + str(hour)

    # For example 1 --> 01
    if len(str(minute)) == 1:
        minute = "0" + str(minute)

    if len(str(month)) == 1:
        month = "0" + str(month)

    if len(str(day)) == 1:
        day = "0" + str(day)


    # DATATIME html format example: 2025-03-11T07:37
    html_time_format = f"{year}-{month}-{day}T{hour}:{minute}"




    if request.method != "POST":
        form_obj = editIncome(initial={"title":title, "price":price, "note":note})

        spend = get_object_or_404(Spend, user=request.user, id=id)
        return render(request, "Spends/edit_spends.html",
                      {"form_obj":form_obj, "spend":spend, 'date':html_time_format})

    else:
        form_obj = editIncome(data=request.POST)

        spend = get_object_or_404(Spend, user=request.user, id=id)
        old_name = spend.title
        spend.title = request.POST['title']
        spend.price = request.POST['price']
        spend.note = request.POST['note']


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


        spend.time = datetime_obj
        spend.save()


        return render(request, "Spends/edit_spend_success.html",
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