from datetime import datetime

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Product(models.Model):
    name = models.CharField(
        max_length=125,
        verbose_name=_('Имя')
    )
    description = models.CharField(max_length=125)
    value = models.DecimalField(
        verbose_name=_('Цена товара'),
        decimal_places=2,
        max_digits=12
    )
    cover = models.ImageField(
        upload_to='media/images',
        verbose_name=_('Главное фото')
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата изменения'),
        auto_now=True
    )
    active = models.BooleanField(
        verbose_name=_('Данный товар активен'),
        default=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class DetailPhotos(models.Model):
    image = models.ImageField(
        verbose_name=_('Детальное фото'),
        upload_to='media/images',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=_('Продукты'),
        related_name='photos'
    )

    class Meta:
        verbose_name = 'Детальное фото'
        verbose_name_plural = 'Детальные фото'


class Stock(models.Model):
    size = models.SmallIntegerField(
        verbose_name=_('Размер'),
        choices=(
            (1, 'S'),
            (2, 'M'),
            (3, 'L'),
            (4, 'XL'),
        ))
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата поступления'),
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата нового поступления'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=_('Продукт'),
        related_name='stocks'
    )

    def __str__(self):
        return f'{self.product}{self.get_size_display()}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склад'

class Order(models.Model):
    status = models.BooleanField(
        verbose_name=_('Статус'),
        default=True)
    total = models.PositiveIntegerField(
        verbose_name=_('Сумма'),
        default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Пользователь'),
    )
    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Склад'),
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата утсановления статуса'),
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата изменения статуса'),
        auto_now=True)

    address = models.CharField(max_length=125)

    def __str__(self):
        return f'{self.stock}{self.user}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderDetail(models.Model):
    quantity = models.PositiveIntegerField(
        verbose_name=_('Количество'),
        default=0
    )
    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
        related_name='order_details',
        verbose_name=_('Склад')
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='order_details',
        verbose_name=_('Заказ')
    )

    class Meta:
        verbose_name = 'Детали заказа'
        verbose_name_plural = 'Детали заказа'
