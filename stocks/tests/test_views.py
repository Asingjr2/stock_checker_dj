from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

from uuid import uuid4

from ..factories import StockFactory, UserFactory

class RefreshAllStocksTestCase(TestCase):
    def test_200(self):
        logged_user = UserFactory()

        client = Client()
        client.force_login(logged_user)
        response = client.get(reverse("stocks:refresh_all"))
        self.assertEqual(response.status_code, 302)

    # Login required so response should be redirect.
    def test_302(self):
        client = Client()
        response = client.get(reverse("stocks:refresh_all"))
        self.assertEqual(response.status_code, 302)
         

class HomeViewTestCase(TestCase):
    def test_200(self):
        logged_user = UserFactory()

        client = Client()
        client.force_login(logged_user)
        response = client.get(reverse("stocks:home"))
        self.assertEqual(response.status_code, 200)

    def test_302(self):
        client = Client()
        response = client.get(reverse("stocks:home"))
        self.assertEqual(response.status_code, 302)


class StockSearchViewTestCase(TestCase):
    def test_200(self):
        logged_user = UserFactory()
        
        client = Client()
        client.force_login(logged_user)
        response = client.get(reverse("stocks:stock_search"))
        self.assertEqual(response.status_code, 200)

    # Login required so response should be redirect.
    def test_302(self):
        client = Client()
        response = client.get(reverse("stocks:stock_search"))
        self.assertEqual(response.status_code, 302)


class CreateAPIViewTestCase(TestCase):
    Access forbidden based on if not authenticated based on permission class.
    def test_403(self):
        data = {}

        url = reverse("rest:create")
        client = Client()
        response = client.get(url, data, follow=True)
        self.assertEqual(response.status_code, 403)


class ListAPIViewTestCase(TestCase):
    def test_200(self):
        client = Client()
        logged_user = UserFactory()
        client.force_login(logged_user)
        response = client.get(reverse("rest:list"))
        self.assertEqual(response.status_code, 200)

    # Access forbidden based on if not authenticated based on permission class.
    def test_403(self):
        client = Client()
        response = client.get(reverse("rest:list"))
        self.assertEqual(response.status_code, 403)


class DeleteAPIViewTestCase(TestCase):
    """ Get method create for url. """

    def test_200(self):
        stock = StockFactory()
        logged_user = UserFactory()

        url = reverse("rest:delete", args=(stock.id,))
        client = Client()
        client.force_login(logged_user)
        response = client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    # Access forbidden based on if not authenticated based on permission class.
    def test_403(self):
        stock = StockFactory()

        url = reverse("rest:delete", args=(stock.id,))
        client = Client()
        response = client.delete(url, follow=True)
        self.assertEqual(response.status_code, 403)

