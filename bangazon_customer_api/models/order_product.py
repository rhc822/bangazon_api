from django.db import models
from .order import Order
from .product import Product

class OrderProduct(models.Model):
    """
        This creates instances of OrderProduct
        - RHC
    """

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)


    class Meta:
        verbose_name = ("order_product")
        verbose_name_plural = ("order_products")

    def __str__(self):
        return f'Order: {self.order.id}\n Product/s: ${self.product.name}'