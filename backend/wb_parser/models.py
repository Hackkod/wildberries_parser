from django.db import models

class Product(models.Model):
    product_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(null=True)
    review_count = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.product_id}: {self.name}'
