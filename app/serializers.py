from rest_framework import serializers

from .models import Product, Stock, DetailPhotos, Order, OrderDetail


class ProductListSerializer(serializers.ModelSerializer):
    value = serializers.DecimalField(
        decimal_places=2,
        max_digits=12
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'cover', 'value')


class SizeSerializer(serializers.ModelSerializer):
    size_name = serializers.CharField(source='get_size_display')

    class Meta:
        model = Stock
        fields = ('size', 'size_name')


class DetailPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailPhotos
        fields = ('image',)


class ProductDetailSerializer(serializers.ModelSerializer):
    stocks = SizeSerializer(many=True)
    detail_photo = DetailPhotoSerializer(many=True, source='photos')

    class Meta:
        model = Product
        fields = ('id', 'name', 'cover', 'description', 'stocks', 'detail_photo', 'value')

    def to_representation(self, instance):
        return super().to_representation(instance)


class StockSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    size = serializers.CharField(source='get_size_display')

    class Meta:
        model = Stock
        fields = ('product', 'size')


class OrderDetailCreateSerializer(serializers.ModelSerializer):
    size = serializers.CharField(write_only=True)
    cap = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderDetail
        exclude = ('order',)


class OrderDetailSerializer(serializers.ModelSerializer):
    stock = StockSerializer()

    class Meta:
        model = OrderDetail
        exclude = ('order',)


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_details = OrderDetailCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ('user', 'order_details', 'address', 'total')

    def create(self, validated_data):
        order = Order(user=validated_data['user'], address=validated_data['address'], total=validated_data['total'])
        order.save()

        for order_detail in validated_data['order_details']:
            OrderDetail(order=order, stock=order_detail['stock'], quantity=order_detail['quantity']).save()

        return order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_details = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ('user', 'order_details')
