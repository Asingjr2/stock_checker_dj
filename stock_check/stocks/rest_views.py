from rest_framework import generics, mixins

from django.contrib.auth.models import User

from stocks.models import Stock, Favorites
from apis.rest_serializer import StockSerializer


class CreateApiView(generics.CreateAPIView):
    lookup_field = "pk"
    serializer_class = StockSerializer

    def get_queryset(self):
        return Stock.objects.all()

    def perform_create(self, serializer):
        user1 = User.objects.first()
        serializer.save(user=user1)


class RetrieveApiView(generics.RetrieveAPIView):
    serializer_class = StockSerializer

    def get_queryset(self):
        return Stock.objects.all()

# Detail view, pk is the standard lookup field
class UpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    serializer_class = StockSerializer

    def get_queryset(self):
        return Stock.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


# List view with create mixin
class ListApiView(mixins.CreateModelMixin,generics.ListAPIView):
    lookup_field = "pk"
    serializer_class = StockSerializer

    # Check out django ordering and filtering with Q
    def get_queryset(self):
        qs = Stock.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(title__icontains=query) |Q(content__icontains=query)).distinct()
        return Stock.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request} 