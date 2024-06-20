from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg

import requests
from datetime import date, datetime

from main.models import Rates
from main.utils import create_rates_range

def rate(request, rate_date=None):

    search_date = rate_date or date.today()

    try:
        rate_obj = Rates.objects.get(date=search_date)
        data = serializers.serialize('json', [rate_obj])
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        pass

    if rate_date:
        url = f"https://api.frankfurter.app/{rate_date}?from=USD&to=EUR"
    else:
        url = "https://api.frankfurter.app/latest?from=USD&to=EUR"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        new_date_string = data["date"]
        new_date = datetime.strptime(new_date_string, "%Y-%m-%d").date()
        new_rate = data["rates"]["EUR"]

        if rate_date and new_date < rate_date:
            create_rates_range(new_date, rate_date, {str(new_date): {"EUR":new_rate}})
        elif not Rates.objects.filter(date=new_date).exists():
            Rates.objects.create(date=new_date, rate=new_rate)

        return JsonResponse(data)
    except requests.RequestException as e:
        return JsonResponse({'error': f'Failed to fetch data from API: {str(e)}'})
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'})



def rate_range(request, start_date, end_date):

    if start_date > end_date:
        return JsonResponse({'error': 'Start date cannot be after the provided end date.'}, status=400)

    try:
        url = f"https://api.frankfurter.app/{str(start_date)}..{str(end_date)}?from=USD&to=EUR"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        rates = data.get("rates", {})

        if str(start_date) not in rates:
            url = f"https://api.frankfurter.app/{start_date}?from=USD&to=EUR"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            date_before_string = data["date"]
            date_before = datetime.strptime(date_before_string, "%Y-%m-%d").date()
            rate_before = {str(date_before): data["rates"]}
            create_rates_range(date_before, start_date, rate_before)


        create_rates_range(start_date, end_date, rates)

        average = Rates.objects.filter(date__range=(start_date, end_date)).aggregate(avg_rate=Avg('rate'))['avg_rate']

        return JsonResponse({'average': average})

    except requests.RequestException as e:
        return JsonResponse({'error': f'Failed to fetch data from API: {str(e)}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)


