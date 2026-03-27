from rest_framework import serializers
from .models import Product, Review, Store


class StoreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Store model.

    Converts Store model instances into JSON format and validates
    incoming data for store-related API operations.
    """

    class Meta:
        model = Store
        fields = ["id", "vendor", "name", "description", "address"]


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    Handles serialization and validation of product data,
    including store relationships and availability.
    """

    class Meta:
        model = Product
        fields = [
            "id",
            "store",
            "name",
            "description",
            "price",
            "stock",
            "available",
            "image",
            "created_at",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Converts review data into JSON format and ensures
    proper validation of user feedback.
    """

    class Meta:
        model = Review
        fields = ["id", "product", "user", "rating", "comment", "created_at"]