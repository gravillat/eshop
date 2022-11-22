from django.contrib import admin
from .models import Product, Order, OrderDetail, Stock, DetailPhotos


class DetailPhotoInline(admin.TabularInline):
    model = DetailPhotos


class CapAdmin(admin.ModelAdmin):
    inlines = [
        DetailPhotoInline,
    ]
    list_display = ['id', 'name', 'is_active', 'cover_image']


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Stock)
admin.site.register(DetailPhotos)










