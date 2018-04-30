from rest_framework import serializers 

from stocks.models import Stock, Favorites


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model= Stock
        fields = ["ticker", "pk"]

    def get_url(self, obj):
        return obj.get_url()

