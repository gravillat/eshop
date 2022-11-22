from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from .serializers import ProductListSerializer, ProductDetailSerializer, StockSerializer, OrderCreateSerializer, \
    OrderSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from .models import Product, Order
from .pagination import CustomPagination


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id', 'value']

    pagination_class = CustomPagination


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name']


class HomePageView(ListAPIView):
    queryset = Product.objects.filter(name='Supreme')
    serializer_class = ProductListSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name']


class OrderListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        elif self.request.method == "GET":
            return OrderSerializer

