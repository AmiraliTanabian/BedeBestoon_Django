from .models import Income, Spend
from django.utils.timezone import now

def month_income_data(request):
    now_month = now().month
    now_year = now().year

    income_objects = Income.objects.filter(user=request.user, time__year=now_year, time__month=now_month)
    income_month = dict.fromkeys(range(1, 13), 0)
    for income in income_objects :
        income_month[income.time.month] += income.price

    return list(income_month.values())

def month_spend_data(request):
    now_month = now().month
    now_year = now().year

    spend_objects = Spend.objects.filter(user=request.user, time__year=now_year, time__month=now_month)
    spend_month = dict.fromkeys(range(1, 13), 0)
    for spend in spend_objects :
        spend_month[spend.time.month] += spend.price


    return list(spend_month.values())


