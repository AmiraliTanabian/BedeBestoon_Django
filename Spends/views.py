import datetime

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Token, Spend, Income, TempUser
from django.utils import timezone
from json.encoder import JSONEncoder
from .forms import registerForm, loginForm, addSpend, addIncome
from secrets import choice
from string import digits, punctuation, ascii_letters
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.db.models import Avg, Sum, Count, Max, Min
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def random_str(length):
    all_letters = digits + punctuation + ascii_letters
    all_letters = all_letters.replace(r'/', '')
    all_letters = all_letters.replace('\\', '')
    result = ''.join(choice(all_letters) for _ in range(length))
    return result

def account_register(request):

    if request.method != 'POST':
        form_object = registerForm()   
        return render(request, 'Spends/register.html', 
                      {'status':False , 'form_object':form_object})
    
    else:
        form_object = registerForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        agian_password = request.POST['again_password']

        if agian_password != password:
            return render(request, 'Spends/register.html', 
                          {'status':'AgianPasswordError', 'form_object':form_object})
        
        elif User.objects.filter(username=username).exists():
            print('Username exists!')
            return render(request, 'Spends/register.html', 
                          {'status':'UserNameExists', 'form_object':form_object})


        elif User.objects.filter(email=email).exists():
            print('Email Exists exists!')
            return render(request, 'Spends/register.html', 
                          {'status':'EmailExists', 'form_object':form_object})
        
        elif form_object.is_valid():
            #TODO; check the user dont on temp users
            #TODO; check ip
            #TODO; remove TempUser
            random_string = random_str(50)

            # Add temp info on table
            TempUser.objects.create(username=username, password=make_password(password),
                                    date=timezone.now() , email=email, random_str=random_string)
            # Send verify email
            verification_url = settings.SITE_URL +  reverse('verify_account', args=[random_string])
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
            return render(request, 'Spends/register.html', {'form_object':form_object})

def verify_account(request, random_string):

    temp_object = TempUser.objects.filter(random_str=random_string)

    if not temp_object.exists():
        print("Salam")
        return render(request, 'Spends/verify_account.html', {'status':'NotFound'})

    elif timezone.now().timestamp() - temp_object[0].date.timestamp() > 12 * 3600 :
        return render(request, 'Spends/verify_account.html', {'status':'Expired'})


    else:
        temp_object = temp_object[0]
        username = temp_object.username
        user_object = User(username=temp_object.username, password=temp_object.password, email=temp_object.email)
        user_object.save()
        this_token = Token(user=user_object, token=random_str(50))
        this_token.save()
        temp_object.delete()
        return render(request, 'Spends/verify_account.html', {'status':'Ok', 'username': username,
                                                              'token':this_token.token})

def login_page(request):
    if request.method != 'POST':
        form_obj = loginForm()
        return render(request, 'Spends/login.html', {'form_obj':form_obj})

    else:
        form_obj = loginForm(data=request.POST)
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

        return render(request, 'Spends/dashboard.html', context)

    else:
        return  render(request, "Spends/home_page.html")

def add_spend(request):
    if request.user.is_authenticated:
        if request.method != "POST":
            add_spend_obj = addSpend()
            context = {'form_obj':add_spend_obj}
            return render(request, 'Spends/add_spend.html', context)

        else:
            add_spend_obj = addSpend(data=request.POST)
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

            Spend.objects.create(user=request.user, title=title, time=datetime_obj, price=price)
            context = {'form_obj': add_spend_obj, 'status': True}
            return render(request, 'Spends/add_spend.html', context)


    else:
        return render(request, 'Spends/unauthorized.html')

def add_income(request):
    if request.user.is_authenticated:
        if request.method != "POST":
            add_income_object = addIncome()
            context = {'form_obj':add_income_object}
            return render(request, 'Spends/add_income.html', context)

        else:
            add_income_object = addIncome(data=request.POST)
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

            Income.objects.create(user=request.user, title=title, time=datetime_obj, price=price)
            context = {'form_obj': add_income_object, 'status': True}
            return render(request, 'Spends/add_income.html', context)


    else:
        return render(request, 'Spends/unauthorized.html')

def header(request):
    context = {"is_login":request.user.is_authenticated}
    return render(request, "Spends/header_component.html", context)

def home_page(request):
    return render(request, "Spends/home_page.html")

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, "Spends/dashboard.html")

    else:
        return render(request, "Spends/unauthorized.html")

def logout_page(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        context = {"username":username}
        return render(request, "Spends/logout.html", context)

    else:
        return render(request, "Spends/logout_without_login.html")
