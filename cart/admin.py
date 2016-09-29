from django.contrib import admin

from .models import CartItem, Cart


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline,
    ]
admin.site.register(Cart, CartAdmin)
