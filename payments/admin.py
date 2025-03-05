from django.contrib import admin
from .models import Item, Order, OrderItem, Discount, Tax


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'is_paid', 'formatted_total_price', 'get_discounts', 'get_taxes')

    def formatted_total_price(self, obj):
        return f"{obj.total_price():.2f}"
    formatted_total_price.short_description = "Сумма заказа"

    def get_discounts(self, obj):
        return ", ".join([f"{d.name} ({d.percentage:.2f}%)" for d in obj.discounts.all()]) if obj.discounts.exists() else "Нет"
    get_discounts.short_description = "Скидки"

    def get_taxes(self, obj):
        return ", ".join([f"{t.name} ({t.percentage:.2f}%)" for t in obj.taxes.all()]) if obj.taxes.exists() else "Нет"
    get_taxes.short_description = "Налоги"


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage')


admin.site.register(Item)
