from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Spends.models import User, Income, Spend, Token
from django.contrib.auth.hashers import  check_password
from json import JSONEncoder
from django.utils import timezone
from django.db.models.aggregates import Avg, Count, Max, Min
from django.http import JsonResponse

@csrf_exempt
def api_general_stats(request):
    token = request.POST['token']
    this_user = Token.objects.get(token=token).user
    income_stats = Income.objects.filter(user=this_user).aggregate(Count('price'), Avg('price'), Max('price'), Min('price'))
    spend_stats = Spend.objects.filter(user=this_user).aggregate(Count('price'), Avg('price'), Max('price'), Min('price'))
    return JsonResponse({'Income':income_stats, 'Spends':spend_stats}, encoder=JSONEncoder)

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password =  request.POST['password']
            user = User.objects.filter(username=username)

            # Username found
            if user :
                # password correct
                user = user[0]
                if check_password(password, user.password):
                    token = Token.objects.get(user=user).token
                    return JsonResponse({"status":"OK", "token":token}, encoder=JSONEncoder)

                # password incorrect
                else:
                    status = 'Password is incorrect'


            # Username not found
            else:
                status = 'Username is incorrect!'
        else:
            status = 'You should send username and password'
    else:
        status = 'Incorrect request (just POST)'

    context = {'status':status}
    return JsonResponse(context, encoder=JSONEncoder)

@csrf_exempt
def api_submit_income(request):
    if request.method == 'POST':
        user = Token.objects.get(token=request.POST['token']).user

        if 'data' not in request.POST :
            date = timezone.now()

        else:
            try:
                date = request.POST['date']
            except :
                return JsonResponse({"Status":"Failed", "Help":"You should send datetime.datime object!"},
                                    encoder=JSONEncoder)

        Income.objects.create(user=user, title=request.POST['title'], price=request.POST['price'],
                              time=date)

    return JsonResponse({'status':'ok'},
                        encoder=JSONEncoder)

@csrf_exempt
def api_submit_spend(request):
    #TODO: data validations : date, token, price, title,...
    if request.method == 'POST':
        user = Token.objects.get(token=request.POST['token']).user
        if 'date' not in request.POST:
            date = timezone.now()


        else:
            try:
                date = request.POST['date']
            except:
                return JsonResponse({"Status": "Failed", "Help": "You should send datetime.datime object!"}
                                    ,encoder=JSONEncoder)

        Spend.objects.create(user=user, title=request.POST['title'],
                            price=request.POST['price'], time=date)

    return JsonResponse({'status':'ok'}, encoder=JSONEncoder)
