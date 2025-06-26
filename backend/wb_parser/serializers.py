from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    discounted_price = serializers.FloatField()
    rating = serializers.FloatField(allow_null=True)
    review_count = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Product
        fields = '__all__'