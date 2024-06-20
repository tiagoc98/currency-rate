from django.shortcuts import get_object_or_404

from main.models import Rates
from datetime import timedelta, date

def create_rates_range(start_date, end_date, rates):

    temp_date = start_date
    first_rate = rates.get(str(start_date), None)

    if not first_rate:
        previous_rate = Rates.objects.filter(date=start_date).first().rate
    else:
        previous_rate = first_rate["EUR"]

    if not previous_rate or (end_date > date.today()) or (start_date > end_date):
        raise Exception

    finish_date = end_date
    if end_date not in rates and end_date == date.today():
        finish_date = end_date - timedelta(days=1)

    while temp_date <= finish_date:

        rate_obj, created = Rates.objects.get_or_create(date=temp_date, defaults={'rate': previous_rate})

        if created:
            rate_obj.rate = previous_rate
            rate_obj.save()

        next_rate = rates.get(str(temp_date), None)
        if next_rate:
            previous_rate = next_rate["EUR"]

        temp_date = temp_date + timedelta(days=1)
