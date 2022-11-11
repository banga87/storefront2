from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Product, Collection, OrderItem
from .serializers import ProductSerializer, CollectionSeralizer


"""
Product Views
"""
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because it is associated with an order item.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)


"""
Collection Views
"""
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSeralizer

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if Collection.objects.annotate(products_count=Count('products')).all() > 0:
            return Response(
                {'error': 'Collection cannot be deleted because a product is associated with it.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)

