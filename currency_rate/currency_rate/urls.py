from django.urls import path, register_converter

from main import views, converters

register_converter(converters.DateConverter, 'date')

urlpatterns = [
    path('rate/<date:start_date>/<date:end_date>/', views.rate_range, name="rate_range"),
    path('rate/<date:rate_date>/', views.rate, name="rate_date"),
    path('rate/', views.rate, name="rate"),
]
