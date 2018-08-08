import time
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

import requests
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from stocks.models import Stock
from apis.rest_serializer import StockSerializer, UserSerializer


class CreateAPIView(generics.CreateAPIView):
    lookup_field = "pk"
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
        today = datetime.today()
        current_time = datetime.now()
        subtract_day = timedelta(days=-1)
        substract_two_days = timedelta(days=-2)

        # Altering time to cover cases where stock market is closed (i.e. Saturday, Sunday, before 9:30 AM EST).  Holidays closures not addressed below.
        if int(current_time.strftime("%H")) < 9 and int(current_time.strftime("%M")) < 31:
            today += subtract_day
        if today.strftime("%A") == "Saturday":
            today += subtract_day
        if today.strftime("%A") == "Sunday":
            today += substract_two_days
        
        # Format used in stock API json response.
        today_formatted = today.strftime("%Y-%m-%d")
     
        ticker = self.request.POST["ticker_symbol"]
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&apikey=HVS4381TKE7Y9YOS"
        resp = requests.get(url).json()['Time Series (Daily)'][today_formatted]
        serializer.save(s_open = round(float(resp["1. open"]),2))
        serializer.save(s_high = round(float(resp["2. high"]),2))
        serializer.save(s_low = round(float(resp["3. low"]),2))
        serializer.save(s_close = round(float(resp["4. close"]),2))
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        response = super( CreateAPIView, self).create(request, *args, **kwargs)
        return HttpResponseRedirect(redirect_to="/stocks/home/")


class ListAPIView(generics.ListAPIView):
    lookup_field = "pk"
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    permission_classes = (IsAuthenticated,)


class DeleteAPIView(generics.DestroyAPIView):
    lookup_field = "pk"
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return HttpResponseRedirect(redirect_to="/stocks/home/")
