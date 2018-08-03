from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.urls import reverse

from base.models import BaseModel


class Stock(BaseModel):
    ticker_symbol = models.CharField(max_length= 4)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return "{} stock ticker".format(self.ticker_symbol)

