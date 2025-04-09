from django.contrib import admin
from .models import Auction, Product, SoldProduct


class ProductInline(admin.TabularInline):
    model = Product
    extra = 3

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ['description', 'date', 'time']
    search_fields = ['description']
    list_filter = ['date', 'time']



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name',  'start_point', 'amount', 'auction']
    list_filter = ['auction']
    search_fields = ['name']

@admin.register(SoldProduct)
class SoldProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'buyer__user__first_name', 'price', 'date']
    list_filter = ['date']
    search_fields = ['product__name', 'buyer__user__username']

