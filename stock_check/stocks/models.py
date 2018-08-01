from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.urls import reverse

from base.models import BaseModel


class Stock(BaseModel):
    ticker_symbol = models.CharField(max_length= 4)

    def __str__(self):
        return "{} stock ticker".format(self.ticker_symbol)

    def get_absolute_url(self, request=None):
        return reverse('rest:retrieve', args=(self.id),)


class Favorites(BaseModel):
    ticker = models.ManyToManyField(Stock)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return "{} is a favorite!".format(self.ticker.ticker_symbol)