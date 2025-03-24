from .models import Income, Spend
from django.utils.timezone import now
from django.db.models.aggregates import Sum

def year_income_data(request):
    now_month = now().month
    now_year = now().year

    income_objects = Income.objects.filter(user=request.user, time__year=now_year, time__month=now_month)
    income_month = dict.fromkeys(range(1, 13), 0)
    for income in income_objects :
        income_month[income.time.month] += income.price

    return list(income_month.values())

def year_spend_data(request):
    now_month = now().month
    now_year = now().year

    spend_objects = Spend.objects.filter(user=request.user, time__year=now_year, time__month=now_month)
    spend_month = dict.fromkeys(range(1, 13), 0)
    for spend in spend_objects :
        spend_month[spend.time.month] += spend.price


    return list(spend_month.values())

def month_income_data(request):
    result = []
    now_yaer = now().year
    now_month = now().month


    for day in range(1, 31):
        current_items = Income.objects.filter(user=request.user, time__year=now_yaer, time__month=now_month ,time__day = day)
        on_day_result = current_items.aggregate(Sum("price")).get("price__sum")
        if on_day_result is None:
            on_day_result = 0

        result.append(on_day_result)

    return result

def month_spend_data(request):
    result = []
    now_yaer = now().year
    now_month = now().month


    for day in range(1, 31):
        current_items = Income.objects.filter(user=request.user, time__year=now_yaer, time__month=now_month, time__day = day)
        on_day_result = current_items.aggregate(Sum("price")).get("price__sum")
        if on_day_result is None:
            on_day_result = 0

        result.append(on_day_result)

    return result

def week_spend_data(request):
    result = []
    now_year = now().year
    now_month = now().month

    for day in range(7):
        week_price = Spend.objects.filter(user=request.user, time__year=now_year, time__month=now_month, time__week_day=day)
        week_price = week_price.aggregate(Sum("price")).get("price__sum")
        if week_price is None:
            week_price = 0
        result.append(week_price)

    # Convert to jalali calender
    j_result = (result[2:6])
    j_result.extend(result[:2])

    return j_result

def week_income_data(request):
    result = []
    now_year = now().year
    now_month = now().month

    for day in range(7):
        week_price = Income.objects.filter(user=request.user, time__year=now_year, time__month=now_month, time__week_day=day)
        week_price = week_price.aggregate(Sum("price")).get("price__sum")
        if week_price is None:
            week_price = 0

        result.append(week_price)

    # Convert to jalali calender
    j_result = (result[2:6])
    j_result.extend(result[:2])

    return j_result

def last_ten_spend_data(request):
    try:
        spends = Spend.objects.filter(user=request.user).order_by("time")[:10]

    except IndexError :
        spends = Spend.objects.filter(user=request.user).order_by("time")

    price_list = [spend.price for spend in spends]
    return price_list

def last_ten_income_data(request):
    try:
        incomes = Income.objects.filter(user=request.user).order_by("time")[:10]

    except IndexError:
        incomes = Income.objects.filter(user=request.user).order_by("time")

    price_list = [income.price for income in incomes]
    return price_list
