from rest_framework.serializers import ModelSerializer

from .models import *

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class AuctionSerializer(ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='product_set')
    class Meta:
        model = Auction
        fields = '__all__'





