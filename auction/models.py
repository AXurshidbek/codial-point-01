from django.db import models


class Auction(models.Model):
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()

    def __str__(self):
        return self.description

class Product(models.Model):
    name=models.CharField(max_length=100)
    start_point=models.PositiveIntegerField()
    image=models.ImageField(upload_to='products/', null=True, blank=True)
    auction=models.ForeignKey(Auction, on_delete=models.CASCADE)
    amount=models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.name} -> ({self.auction.date})"


class SoldProduct(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer=models.ForeignKey('main.Student', on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.buyer.user.first_name} {self.buyer.user.last_name} ({self.price})"

    def save(self, *args, **kwargs):
        if self.price < self.product.start_point:
            raise ValueError("Price must be greater than the starting point of the product.")

        if self.pk:

            prev_instance = SoldProduct.objects.select_related('product', 'buyer').get(pk=self.pk)
            prev_instance.product.amount += 1
            prev_instance.buyer.point += prev_instance.price
            prev_instance.product.save()
            prev_instance.buyer.save()

        self.product.amount -= 1
        self.buyer.point -= self.price
        self.product.save()
        self.buyer.save()

        super().save(*args, **kwargs)