from django.db import models
from decimal import Decimal


class Discount(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Скидка в процентах")
    stripe_coupon_id = models.CharField(max_length=255, null=True, blank=True)

    def apply_discount(self, amount):
        return amount - (amount * self.percentage / 100)

    def __str__(self):
        return f"{self.name} - {self.percentage:.2f}%"


class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Налог в процентах")
    stripe_tax_rate_id = models.CharField(max_length=255, null=True, blank=True)

    def apply_tax(self, amount):
        return amount + (amount * self.percentage / 100)

    def __str__(self):
        return f"{self.name} - {self.percentage:.2f}%"


class Item(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    def __str__(self):
        return f"{self.name} - {self.price} {self.currency}"


class Order(models.Model):
    items = models.ManyToManyField('Item', through='OrderItem')
    discounts = models.ManyToManyField('Discount', blank=True)
    taxes = models.ManyToManyField('Tax', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    currency = models.CharField(max_length=3, choices=Item.CURRENCY_CHOICES, default='usd')

    def total_price(self):
        base_price = sum(order_item.item.price * order_item.quantity for order_item in self.orderitem_set.all())

        for discount in self.discounts.all():
            base_price = discount.apply_discount(base_price)

        for tax in self.taxes.all():
            base_price = tax.apply_tax(base_price)

        return Decimal(base_price).quantize(Decimal("0.01"))

    def __str__(self):
        return f"Order #{self.id} - Total: ${self.total_price():.2f} {self.currency}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} (x{self.quantity})"