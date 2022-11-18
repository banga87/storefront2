from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .filters import ProductFilter
from .models import Product, Collection, OrderItem, Review, Cart, CartItem
from .pagination import DefaultPagination
from .serializers import ProductSerializer, CollectionSeralizer, ReviewSerializer, CartSerializer, CartItemSerializer


"""
Product Views
"""
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

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


"""
Review Views
"""
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    # Overriden to filter by the product_id stored in the url
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    # Accesses the product_pk from the URL and enables us to access in our serializer.
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


"""
Cart Views
"""
class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  ListModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


"""
CartItem Views
"""
class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    # Overriden to filter by the cart_id stored in the URL
    def get_queryset(self):
        return CartItem.objects. \
            filter(cart_id=self.kwargs['cart_pk']). \
            select_related('product')

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}