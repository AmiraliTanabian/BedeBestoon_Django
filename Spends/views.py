from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Token, Spend, Income, TempUser
from django.utils import timezone
from json.encoder import JSONEncoder
from .forms import registerForm
from secrets import choice
from string import digits, punctuation, ascii_letters
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.db.models import Avg, Sum, Count, Max, Min

def random_str(length):
    all_letters = digits + punctuation + ascii_letters
    all_letters = all_letters.replace(r'/', '')
    all_letters = all_letters.replace('\\', '')
    result = ''.join(choice(all_letters) for _ in range(length))
    return result


@csrf_exempt
def api_submit_spend(request):
    #TODO: data validations : date, token, price, title,...
    if request.method == 'POST':
        user = Token.objects.get(token=request.POST['token']).user
        if 'date' not in request.POST:
            date = timezone.now()

        else:
            date = request.POST['date']

        Spend.objects.create(user=user, title=request.POST['title'],
                            price=request.POST['price'], time=date)

    return JsonResponse({'status':'ok'}, encoder=JSONEncoder)

@csrf_exempt
def api_submit_income(request):
    print(request.POST['token'])
    if request.method == 'POST':
        user = Token.objects.get(token=request.POST['token']).user

        if 'data' not in request.POST :
            date = timezone.now()

        else:
            date = request.POST['date']

        Income.objects.create(user=user, title=request.POST['title'], price=request.POST['price'],
                              time=date)

    return JsonResponse({'status':'ok'},
                        encoder=JSONEncoder)

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
#     tau5-L3__>}vXzE7$LbwlQH96g7M[d+$H?|w)2Iq?08]08^l'#
@csrf_exempt
def general_stats(request):
    token = request.POST['token']
    print(Token.objects.filter(token=token).exists())
    this_user = Token.objects.get(token=token).user
    income_stats = Income.objects.filter(user=this_user).aggregate(Count('price'), Avg('price'), Max('price'), Min('price'))
    spend_stats = Spend.objects.filter(user=this_user).aggregate(Count('price'), Avg('price'), Max('price'), Min('price'))
    return JsonResponse({'Income':income_stats, 'Spends':spend_stats}, encoder=JSONEncoder)