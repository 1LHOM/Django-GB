from django.db import models
from django.conf import settings

from mainapp.models import Product


class Order(models.Model):

    STATUS_FORMING = 'FM'
    STATUS_SEND_TO_PROCEED = 'STP'
    STATUS_PROCEEDED = 'PD'
    STATUS_PAID = 'PD'
    STATUS_CANCEL = 'CNL'
    STATUS_DONE = 'DN'

    STATUSES = (
        (STATUS_FORMING, 'формируется'),
        (STATUS_SEND_TO_PROCEED, 'отправлено в обработку'),
        (STATUS_PROCEEDED, 'обработано'),
        (STATUS_PAID, 'оплачено'),
        (STATUS_CANCEL, 'отменено'),
        (STATUS_DONE, 'завершено'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, default=STATUS_FORMING, max_length=5)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_quantity(self):
        _items = self.orderitems.select_related()
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    def get_total_cost(self):
        _items = self.orderitems.select_related()
        _total_cost = sum(list(map(lambda x: x.quantity * x.product.price, _items)))
        return _total_cost

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    def get_product_cost(self):
        return self.product.price * self.quantity
