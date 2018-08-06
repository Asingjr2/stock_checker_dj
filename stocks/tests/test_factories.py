from django.test import TestCase

import factory

from ..factories import StockFactory, UserFactory
from base.factories import BaseModelFactory

class StockFactoryTestCase(TestCase):
    def test_factory(self):
        stock = StockFactory()

        self.assertIsNotNone(stock.ticker_symbol)
        self.assertIsNotNone(stock.s_open)
        self.assertIsNotNone(stock.s_close)
        self.assertIsNotNone(stock.s_high)
        self.assertIsNotNone(stock.s_low)
        self.assertIsNotNone(stock.user)