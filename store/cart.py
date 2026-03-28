from decimal import Decimal
from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0}

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart_copy = self.cart.copy()

        for product in products:
            cart_copy[str(product.id)]["product"] = product
            cart_copy[str(product.id)]["price"] = product.price
            cart_copy[str(product.id)]["total_price"] = (
                product.price * cart_copy[str(product.id)]["quantity"]
            )
            yield cart_copy[str(product.id)]

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        total = Decimal("0.00")
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            total += product.price * self.cart[str(product.id)]["quantity"]

        return total

    def clear(self):
        del self.session["cart"]
        self.save()