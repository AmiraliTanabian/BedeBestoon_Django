from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Token, Spend, Income
from datetime import datetime
from json.encoder import JSONEncoder

@csrf_exempt
def submit_spend(request):

    print(request.POST['token'])
    #TODO: data validations : date, token, price, title,...
    if request.method == 'POST':
        user = Token.objects.get(token=request.POST['token']).user
        if 'date' not in request.POST:
            date = datetime.now()

        else:
            date = request.POST['date']

        Spend.objects.create(user=user, title=request.POST['title'],
                            price=request.POST['price'], time=date)

    return JsonResponse({'status':'ok'}, encoder=JSONEncoder)