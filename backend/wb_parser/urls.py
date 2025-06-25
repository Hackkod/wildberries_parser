from django.urls import path
from .views import ProductListView, ProductParseView

urlpatterns = [
    path(route='products/', view=ProductListView.as_view(), name='products'),
    path(route='products/parse/', view=ProductParseView.as_view(), name='products-parse'),
]
