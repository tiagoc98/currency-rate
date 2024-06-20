from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from decimal import Decimal

from main.models import Rates

class RateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('rate')

    def test_rate(self):
        response = self.client.get(self.url)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rates.objects.all().count(), 1)

        second_response = self.client.get(self.url)
        second_data = second_response.json()

        self.assertFalse(data == second_data)
        self.assertEqual(Rates.objects.all().count(), 1)

    def test_rate_date(self):
        date_str = '2024-06-18'
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        url = reverse('rate_date', args=[date])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rates.objects.all().count(), 1)

        rate = Rates.objects.all().first()
        self.assertEqual(rate.date, date)
        self.assertEqual(rate.rate, Decimal("0.93327")) # value recorded for this currency rate on 2024-06-18

        second_response = self.client.get(url)
        second_data = second_response.json()

        self.assertFalse(data == second_data)
        self.assertEqual(Rates.objects.all().count(), 1)

    def test_rate_date_missing_rate(self):
        date_str = '2024-01-01'
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        url = reverse('rate_date', args=[date])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rates.objects.all().count(), 4)

        rate = Rates.objects.all().first()
        self.assertEqual(str(rate.date), data["date"])
        self.assertEqual(rate.rate, Decimal("0.90498")) # value recorded for this currency rate on 2023-12-29 the previous rate provided

        second_response = self.client.get(url)
        second_data = second_response.json()

        self.assertFalse(data == second_data)
        self.assertEqual(Rates.objects.all().count(), 4)

    def test_rate_range_average(self):
        start_date_str = '2023-12-27'
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

        end_date_str = '2024-01-05'
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        url = reverse('rate_range', args=[start_date, end_date])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rates.objects.all().count(), 10)
        sum = 0
        for obj in Rates.objects.all():
            sum += obj.rate
        average = sum/10
        self.assertEqual(Decimal(data["average"]), average)

    def test_rate_date_missing_rate(self):
        date_str = '2024-01-01'
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        url = reverse('rate_date', args=[date])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rates.objects.all().count(), 4)

        rate = Rates.objects.all().first()
        self.assertEqual(str(rate.date), data["date"])
        self.assertEqual(rate.rate, Decimal("0.90498")) # value recorded for this currency rate on 2023-12-29 the previous rate provided

        second_response = self.client.get(url)
        second_data = second_response.json()

        self.assertFalse(data == second_data)
        self.assertEqual(Rates.objects.all().count(), 4)

    def test_rate_range_average_no_first_value(self):
        start_date_str = '2024-01-01'
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

        end_date_str = '2024-01-05'
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        url = reverse('rate_range', args=[start_date, end_date])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rates.objects.all().count(), 8) # previous rate available is 2023-12-29
        sum = 0
        for obj in Rates.objects.filter(date__range=(start_date, end_date)):
            sum += obj.rate
        average = sum/5
        self.assertEqual(Decimal(data["average"]), average)



