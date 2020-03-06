from django.db import models
from .customer import Customer
from safedelete.models import SafeDeleteModel
from safedelete.models import HARD_DELETE_NOCASCADE


class PaymentType(SafeDeleteModel):
    """ This model is for payment types. Created by Erin Polley, Esq."""
    _safedelete_policy = HARD_DELETE_NOCASCADE

    merchant_name = models.CharField(max_length=25)
    acct_number = models.CharField(max_length=25)
    expiration_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)



    class Meta:
        ordering = ("-created_at",)
        verbose_name = ("payment_type")
        verbose_name_plural = ("payment_types")

    def __str__(self):
        return f'Merchant Name--{self.merchant_name}. Account Number--{self.acct_number}. Expiration Date--{self.expiration_date}'
