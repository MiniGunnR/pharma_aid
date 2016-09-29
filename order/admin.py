from django.contrib import admin

from .models import Order, OrderItem, RequestedProduct, Prescription


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('product', 'price')
        return self.readonly_fields


class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Order Info', {'fields': (('transaction_id', 'user'), ('status', 'ip_address'))}),

        ('Contact Info', {'fields': (('email', 'mobile'),)}),

        ('Shipping Info', {'fields': ('shipping_name', 'shipping_address_1', 'shipping_address_2', ('shipping_city', 'shipping_zip'), 'shipping_country')}),

        ('Billing Info', {'classes': ('collapse',), 'fields': ('billing_name', 'billing_address_1', 'billing_address_2', ('billing_city', 'billing_zip'), 'billing_country')}),

        ('Delivery Info', {'fields': (('delivery_time', 'delivery_charge'),)}),

        ('Payment Info', {'fields': (('payment_method', 'trx_id'),)}),
    )

    inlines = [
        OrderItemInline,
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('user', 'transaction_id', 'ip_address') + ('email', 'mobile') + \
                   ('shipping_name', 'shipping_address_1', 'shipping_address_2', 'shipping_city', 'shipping_zip', 'shipping_country') + \
                   ('billing_name', 'billing_address_1', 'billing_address_2', 'billing_city', 'billing_zip', 'billing_country') + \
                   ('delivery_charge',)
        return self.readonly_fields

admin.site.register(Order, OrderAdmin)

admin.site.register(RequestedProduct)
admin.site.register(Prescription)