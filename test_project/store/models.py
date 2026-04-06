"""
Database models for the eCommerce application.

Defines users' profiles, vendor stores, products, orders,
reviews, and password reset tokens.
"""

from decimal import Decimal
from datetime import timedelta
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    """
    Represents a user profile with an assigned role.

    Each user is associated with a profile that determines
    whether they act as a buyer or vendor within the system.
    """

    ROLE_CHOICES = (
        ("buyer", "Buyer"),
        ("vendor", "Vendor"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        """Return a readable representation of the profile."""
        return f"{self.user.username} - {self.role}"


class Store(models.Model):
    """
    Represents a vendor-owned store.

    Each store belongs to a vendor and contains multiple products.
    """

    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stores")
    name = models.CharField(max_length=150)
    description = models.TextField()
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Define default ordering for stores."""
        ordering = ["name"]

    def __str__(self):
        """Return the store name."""
        return self.name


class Product(models.Model):
    """
    Represents a product sold by a store.

    Each product is associated with exactly one store.
    """

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Define default ordering for products."""
        ordering = ["name"]

    def __str__(self):
        """Return product name with its store."""
        return f"{self.name} ({self.store.name})"


class Order(models.Model):
    """
    Represents a customer order.

    Stores customer details, order status, invoice number,
    and the total price of the order.
    """

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        """Define default ordering for orders."""
        ordering = ["-created_at"]

    def __str__(self):
        """Return a readable order summary."""
        return f"Order #{self.id} - {self.full_name}"

    def save(self, *args, **kwargs):
        """
        Automatically generate an invoice number if not set.
        """
        if not self.invoice_number:
            self.invoice_number = (
                f"INV-{timezone.now().strftime('%Y%m%d%H%M%S')}-"
                f"{uuid.uuid4().hex[:6].upper()}"
            )
        super().save(*args, **kwargs)

    def update_total(self):
        """
        Recalculate and update the total price of the order.
        """
        total = sum(item.subtotal() for item in self.items.all())
        self.total_price = total
        self.save(update_fields=["total_price"])


class OrderItem(models.Model):
    """
    Represents a single item within an order.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Return a readable description of the order item."""
        product_name = self.product.name if self.product else "Deleted Product"
        return f"{product_name} x {self.quantity}"

    def subtotal(self):
        """Calculate the subtotal for this item."""
        return self.price * self.quantity


class Review(models.Model):
    """
    Represents a product review submitted by a user.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True)
    verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Define default ordering for reviews."""
        ordering = ["-created_at"]

    def __str__(self):
        """Return a readable review summary."""
        return f"Review by {self.user.username} for {self.product.name}"


class ResetToken(models.Model):
    """
    Represents a password reset token.

    Tokens expire after a defined period and can only be used once.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reset_tokens",
    )
    token = models.CharField(max_length=40, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Automatically set expiry time if not provided.
        """
        if not self.expiry_date:
            self.expiry_date = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)

    def is_expired(self):
        """Check whether the token has expired."""
        return timezone.now() > self.expiry_date

    def __str__(self):
        """Return a readable token representation."""
        return f"{self.user.username} reset token"