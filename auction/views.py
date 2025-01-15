from rest_framework.generics import *
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated



class AuctionListView(ListAPIView):
    queryset = Auction.objects.all().order_by('date', 'time')
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]

class AuctionCreateView(CreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]

class AuctionDetailView(ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]


class CurrentAuctionDetailView(RetrieveAPIView):
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Auction.objects.order_by('-date','-time')

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.first()

class CurrentAuctionProductsView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        latest_auction = Auction.objects.order_by('-date', '-time').first()
        if latest_auction is None:
            return Product.objects.none()

        return Product.objects.filter(auction=latest_auction)


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        auction_id = self.kwargs.get('pk')
        return Product.objects.filter(auction_id=auction_id)



