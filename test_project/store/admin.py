"""
Admin configuration for the store application.
"""

from django.contrib import admin

from .models import Order, OrderItem, Product, Profile, ResetToken, Review, Store


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for user profiles.
    """

    list_display = ("user", "role")
    search_fields = ("user__username", "role")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """
    Admin configuration for stores.
    """

    list_display = ("name", "vendor", "created_at")
    search_fields = ("name", "vendor__username")
    list_filter = ("created_at",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for products.
    """

    list_display = ("name", "store", "price", "stock", "available", "created_at")
    search_fields = ("name", "store__name")
    list_filter = ("available", "created_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for orders.
    """

    list_display = ("id", "full_name", "email", "status", "total_price", "created_at")
    search_fields = ("full_name", "email", "invoice_number")
    list_filter = ("status", "created_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for order items.
    """

    list_display = ("order", "product", "quantity", "price")
    search_fields = ("order__id", "product__name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for reviews.
    """

    list_display = ("user", "product", "rating", "verified_purchase", "created_at")
    search_fields = ("user__username", "product__name")
    list_filter = ("rating", "verified_purchase", "created_at")


@admin.register(ResetToken)
class ResetTokenAdmin(admin.ModelAdmin):
    """
    Admin configuration for password reset tokens.
    """

    list_display = ("user", "token", "created_at", "expiry_date", "used")
    search_fields = ("user__username", "token")
    list_filter = ("used", "created_at", "expiry_date")