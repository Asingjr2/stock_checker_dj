from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

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
        redirect("/stocks/home/")
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
