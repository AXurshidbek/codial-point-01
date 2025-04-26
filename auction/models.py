from django.db import models
from django.db.models import F
from django.db import transaction
from main.models import Student


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


            Product.objects.filter(id=prev_instance.product.id).update(amount=F('amount') + 1)
            Student.objects.filter(id=prev_instance.buyer.id).update(point=F('point') + prev_instance.price)


        Product.objects.filter(id=self.product.id).update(amount=F('amount') - 1)
        Student.objects.filter(id=self.buyer.id).update(point=F('point') - self.price)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            Product.objects.filter(id=self.product.id).update(amount=F('amount') + 1)
            Student.objects.filter(id=self.buyer.id).update(point=F('point') + self.price)
            super().delete(*args, **kwargs)