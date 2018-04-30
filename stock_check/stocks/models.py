from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.urls import reverse


from base.models import BaseModel

class Stock(BaseModel):
    ticker = models.CharField(max_length= 4)

    def __str__(self):
        return "{} stock ticker".format(self.ticker)

    def get_url(self, request=None):
        return reverse('rest:retrieve', args=(self.id),)

class Favorites(BaseModel):
    ticker = models.ManyToManyField(Stock)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return "{} list of favorites currntly has {} stocks".format(self.user.username, self.stock.ticker)