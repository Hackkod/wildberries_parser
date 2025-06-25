from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer
from .utils.parser import parse_and_save_products


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'discounted_price', 'rating', 'review_count', 'name']
    ordering = ['price']

class ProductParseView(APIView):
    def post(self, request):
        query = request.data.get("query")
        if not query:
            return Response({"error": "Необходимо указать 'query'"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            imported_count = parse_and_save_products(query)
            return Response({"parser result": imported_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
