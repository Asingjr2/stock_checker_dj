from django.contrib.auth.models import User

import factory
from factory.fuzzy import FuzzyDecimal, FuzzyText

from .models import Stock

from base.factories import BaseModelFactory


class UserFactory(BaseModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user{}'.format(n))
    password = FuzzyText(length=10)


class StockFactory(BaseModelFactory):
    class Meta:
        model = Stock

    ticker_symbol = FuzzyText(length=4)
    s_open = FuzzyDecimal(.01, 5000)
    s_close = FuzzyDecimal(.01, 5000)
    s_high = FuzzyDecimal(.01, 5000)
    s_low = FuzzyDecimal(.01, 5000)
    user = factory.SubFactory(UserFactory)

