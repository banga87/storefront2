from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, CollectionSeralizer, ReviewSerializer


"""
Product Views
"""
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # build a queryset
        queryset = Product.objects.all()
        # search for collection_id
        collection_id = self.request.query_params.get('collection_id')
        # check if collection_id exists
        if collection_id is not None:
            # filter queryset if it does
            queryset = queryset.filter(collection_id=collection_id)
        # return queryset
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because an orderitem is associated with it.'},
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


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    # accesses the product_pk from the URL and enables us to access in our serializer.
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
