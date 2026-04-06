"""
Views for the eCommerce application.

This module contains authentication, dashboard, store, product,
cart, checkout, password reset, and API-related views.
"""

import json
import secrets
from datetime import timedelta
from decimal import Decimal
from hashlib import sha1

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .cart import Cart
from .forms import (
    CartAddProductForm,
    CheckoutForm,
    LoginForm,
    ProductForm,
    RegisterForm,
    StoreForm,
)
from .functions.reddit import get_reddit_posts
from .models import Order, OrderItem, Product, Profile, ResetToken, Review, Store
from .serializers import ProductSerializer, ReviewSerializer, StoreSerializer


def home(request):
    """
    Render the home page.
    """
    return render(request, "store/home.html")


def register_user(request):
    """
    Register a new user and assign the selected role.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data["role"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, "store/register.html", {"form": form})

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return render(request, "store/register.html", {"form": form})

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            Profile.objects.create(user=user, role=role)

            if role == "vendor":
                try:
                    vendors_group = Group.objects.get(name="Vendors")
                    user.groups.add(vendors_group)
                except Group.DoesNotExist:
                    pass
            else:
                try:
                    buyers_group = Group.objects.get(name="Buyers")
                    user.groups.add(buyers_group)
                except Group.DoesNotExist:
                    pass

            login(request, user)

            if role == "vendor":
                return redirect("store:vendor_dashboard")
            return redirect("store:buyer_dashboard")
    else:
        form = RegisterForm()

    return render(request, "store/register.html", {"form": form})


def login_user(request):
    """
    Authenticate and log in a user.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if hasattr(user, "profile") and user.profile.role == "vendor":
                    return redirect("store:vendor_dashboard")
                return redirect("store:buyer_dashboard")

            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "store/login.html", {"form": form})


def logout_user(request):
    """
    Log out the current user.
    """
    logout(request)
    return redirect("store:login")


@login_required
def buyer_dashboard(request):
    """
    Display the buyer dashboard for users with the buyer role.
    """
    if not hasattr(request.user, "profile") or request.user.profile.role != "buyer":
        messages.error(request, "You do not have access to this page.")
        return redirect("store:home")
    return render(request, "store/buyer_dashboard.html")


@login_required
def vendor_dashboard(request):
    """
    Display the vendor dashboard for users with the vendor role.
    """
    if not hasattr(request.user, "profile") or request.user.profile.role != "vendor":
        messages.error(request, "You do not have access to this page.")
        return redirect("store:home")
    return render(request, "store/vendor_dashboard.html")


@login_required
def vendor_store_list(request):
    """
    Display all stores owned by the current vendor.
    """
    if not hasattr(request.user, "profile") or request.user.profile.role != "vendor":
        messages.error(request, "You do not have access to this page.")
        return redirect("store:home")

    stores = Store.objects.filter(vendor=request.user)
    return render(request, "store/vendor_store_list.html", {"stores": stores})


@login_required
def store_create(request):
    """
    Create a new store for the current vendor.
    """
    if not hasattr(request.user, "profile") or request.user.profile.role != "vendor":
        messages.error(request, "You do not have access to this page.")
        return redirect("store:home")

    if request.method == "POST":
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.vendor = request.user
            store.save()
            messages.success(request, "Store created successfully.")
            return redirect("store:vendor_store_list")
    else:
        form = StoreForm()

    return render(request, "store/store_form.html", {"form": form, "title": "Create Store"})


@login_required
def store_update(request, pk):
    """
    Update a store owned by the current vendor.
    """
    if not hasattr(request.user, "profile") or request.user.profile.role != "vendor":
        messages.error(request, "You do not have access to this page.")
        return redirect("store:home")

    store = get_object_or_404(Store, pk=pk, vendor=request.user)

    if request.method == "POST":
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, "Store updated successfully.")
            return redirect("store:vendor_store_list")
    else:
        form = StoreForm(instance=store)

    return render(request, "store/store_form.html", {"form": form, "title": "Edit Store"})


@login_required
def store_delete(request, pk):
    """
    Delete a store owned by the current vendor.
    """
    if not hasattr(request.user, "profile") or request.user.profile.role != "vendor":
        messages.error(request, "You do not have access to this page.")
        return redirect("store:home")

    store = get_object_or_404(Store, pk=pk, vendor=request.user)

    if request.method == "POST":
        store.delete()
        messages.success(request, "Store deleted successfully.")
        return redirect("store:vendor_store_list")

    return render(request, "store/store_delete.html", {"store": store})


@login_required
def vendor_product_list(request):
    """
    Display all products belonging to the current vendor's stores.
    """
    if not hasattr(request.user, "profile") or request.user.profile.role != "vendor":
        messages.error(request, "You do not have access to this page.")
        return redirect("store:home")

    products = Product.objects.filter(store__vendor=request.user)
    return render(request, "store/vendor_product_list.html", {"products": products})


@login_required
def product_create(request):
    """
    Create a new product for one of the current vendor's stores.
    """
    if not hasattr(request.user, "profile") or request.user.profile.role != "vendor":
        messages.error(request, "You do not have access to this page.")
        return redirect("store:home")

    vendor_stores = Store.objects.filter(vendor=request.user)

    if not vendor_stores.exists():
        messages.error(request, "You must create a store before adding a product.")
        return redirect("store:create_store")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        form.fields["store"].queryset = vendor_stores

        if form.is_valid():
            product = form.save(commit=False)

            if product.store.vendor != request.user:
                messages.error(request, "You can only add products to your own stores.")
                return redirect("store:vendor_product_list")

            product.save()
            messages.success(request, "Product created successfully.")
            return redirect("store:vendor_product_list")
    else:
        form = ProductForm()
        form.fields["store"].queryset = vendor_stores

    return render(request, "store/product_form.html", {"form": form, "title": "Create Product"})


@login_required
def product_update(request, pk):
    """
    Update a product belonging to one of the current vendor's stores.
    """
    if not hasattr(request.user, "profile") or request.user.profile.role != "vendor":
        messages.error(request, "You do not have access to this page.")
        return redirect("store:home")

    product = get_object_or_404(Product, pk=pk, store__vendor=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        form.fields["store"].queryset = Store.objects.filter(vendor=request.user)

        if form.is_valid():
            updated_product = form.save(commit=False)

            if updated_product.store.vendor != request.user:
                messages.error(request, "You can only edit products in your own stores.")
                return redirect("store:vendor_product_list")

            updated_product.save()
            messages.success(request, "Product updated successfully.")
            return redirect("store:vendor_product_list")
    else:
        form = ProductForm(instance=product)
        form.fields["store"].queryset = Store.objects.filter(vendor=request.user)

    return render(request, "store/product_form.html", {"form": form, "title": "Edit Product"})


@login_required
def product_delete(request, pk):
    """
    Delete a product belonging to one of the current vendor's stores.
    """
    if not hasattr(request.user, "profile") or request.user.profile.role != "vendor":
        messages.error(request, "You do not have access to this page.")
        return redirect("store:home")

    product = get_object_or_404(Product, pk=pk, store__vendor=request.user)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect("store:vendor_product_list")

    return render(request, "store/product_delete.html", {"product": product})


@login_required
def store_list(request):
    """
    Display all stores.
    """
    stores = Store.objects.all()
    return render(request, "store/store_list.html", {"stores": stores})


@login_required
def store_detail(request, store_id):
    """
    Display one store and its available products.
    """
    store = get_object_or_404(Store, pk=store_id)
    products = store.products.filter(available=True)
    return render(request, "store/store_products.html", {"store": store, "products": products})


@login_required
def product_list(request):
    """
    Display all available products.
    """
    products = Product.objects.filter(available=True)
    return render(request, "store/product_list.html", {"products": products})


@login_required
def product_detail(request, product_id):
    """
    Display details for a single available product.
    """
    product = get_object_or_404(Product, pk=product_id, available=True)
    reviews = Review.objects.filter(product=product)
    form = CartAddProductForm()
    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "form": form,
        },
    )


@login_required
def create_store(request):
    """
    Alias view for store creation.
    """
    return store_create(request)


@login_required
def create_product(request):
    """
    Alias view for product creation.
    """
    return product_create(request)


@require_POST
def cart_add(request, product_id):
    """
    Add a product to the shopping cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd["quantity"],
            override_quantity=cd["override"],
        )

    return redirect("store:cart_detail")


def cart_remove(request, product_id):
    """
    Remove a product from the shopping cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("store:cart_detail")


def cart_detail(request):
    """
    Display the current contents of the shopping cart.
    """
    cart = Cart(request)

    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={
                "quantity": item["quantity"],
                "override": True,
            }
        )

    return render(request, "store/cart.html", {"cart": cart})


@login_required
def checkout(request):
    """
    Process checkout and create an order from the shopping cart.
    """
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect("store:cart_detail")

    cart_items = []
    total = Decimal("0.00")

    for item in cart:
        product = item["product"]
        quantity = item["quantity"]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user

            order.total_price = total
            order.status = "paid"
            order.save()

            for item in cart_items:
                product = item["product"]
                quantity = item["quantity"]

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                )

                if product.stock >= quantity:
                    product.stock -= quantity
                    if product.stock == 0:
                        product.available = False
                    product.save()

            cart.clear()
            messages.success(request, "Your order has been placed successfully.")

            send_mail(
                subject=f"Invoice for Order #{order.id}",
                message=f"Thank you for your order. Your total was ${total}.",
                from_email=None,
                recipient_list=[order.email],
                fail_silently=True,
            )

            return redirect("store:order_success", order_id=order.id)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data["full_name"] = request.user.get_full_name()
            initial_data["email"] = request.user.email

        form = CheckoutForm(initial=initial_data)

    return render(
        request,
        "store/checkout.html",
        {
            "form": form,
            "cart_items": cart_items,
            "total": total,
        },
    )


@login_required
def order_success(request, order_id):
    """
    Display order success details for the current user.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "store/order_success.html", {"order": order})


@login_required
def order_list(request):
    """
    Display all orders for the current user.
    """
    orders = Order.objects.filter(user=request.user).order_by("-id")
    return render(request, "store/order_list.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    """
    Display one order and its items for the current user.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    return render(
        request,
        "store/order_detail.html",
        {
            "order": order,
            "order_items": order_items,
        },
    )


def build_reset_email(user, reset_url):
    """
    Build the password reset email message for a user.
    """
    subject = "Password Reset"
    body = f"Hi {user.username},\n\nUse this link to reset your password:\n{reset_url}"
    return EmailMessage(subject, body, "noreply@example.com", [user.email])


def generate_reset_url(request, user):
    """
    Generate and store a password reset token, then return the reset URL.
    """
    raw_token = secrets.token_urlsafe(16)
    hashed_token = sha1(raw_token.encode()).hexdigest()
    expiry_date = timezone.now() + timedelta(minutes=10)

    ResetToken.objects.create(
        user=user,
        token=hashed_token,
        expiry_date=expiry_date,
        used=False,
    )

    return request.build_absolute_uri(reverse("store:reset_user_password", args=[raw_token]))


def forgot_password(request):
    """
    Handle password reset requests by email.
    """
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            reset_url = generate_reset_url(request, user)
            email_message = build_reset_email(user, reset_url)
            email_message.send()
            return render(
                request,
                "store/forgot_password.html",
                {"success": "Password reset email sent."},
            )
        except User.DoesNotExist:
            return render(
                request,
                "store/forgot_password.html",
                {"error": "No account found with that email."},
            )

    return render(request, "store/forgot_password.html")


def reset_user_password(request, token):
    """
    Validate a password reset token and render the reset form.
    """
    hashed_token = sha1(token.encode()).hexdigest()

    try:
        user_token = ResetToken.objects.get(token=hashed_token, used=False)

        if user_token.expiry_date < timezone.now():
            user_token.delete()
            return render(
                request,
                "store/password_reset.html",
                {"error": "This reset link has expired."},
            )

        request.session["reset_user"] = user_token.user.username
        request.session["reset_token"] = token
        return render(request, "store/password_reset.html")

    except ResetToken.DoesNotExist:
        return render(
            request,
            "store/password_reset.html",
            {"error": "Invalid reset link."},
        )


def reset_password(request):
    """
    Update the user's password after validating the reset session.
    """
    if request.method == "POST":
        username = request.session.get("reset_user")
        token = request.session.get("reset_token")
        password = request.POST.get("password")
        password_conf = request.POST.get("password_conf")

        if not username or not token:
            return redirect("store:forgot_password")

        if password != password_conf:
            return render(
                request,
                "store/password_reset.html",
                {"error": "Passwords do not match."},
            )

        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()

            hashed_token = sha1(token.encode()).hexdigest()
            reset_token = ResetToken.objects.get(token=hashed_token)
            reset_token.used = True
            reset_token.save()

            request.session.pop("reset_user", None)
            request.session.pop("reset_token", None)

            return redirect("store:login")
        except User.DoesNotExist:
            return render(
                request,
                "store/password_reset.html",
                {"error": "User not found."},
            )

    return redirect("store:forgot_password")


def api_product_list(request):
    """
    Return a JSON list of all products.
    """
    products = Product.objects.all().values()
    return JsonResponse(list(products), safe=False)


def api_product_detail(request, pk):
    """
    Return JSON details for a single product.
    """
    try:
        product = Product.objects.get(pk=pk)
        data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "stock": product.stock,
            "available": product.available,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)


@csrf_exempt
def api_product_create(request):
    """
    Create a product through the basic JSON API.
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    data = json.loads(request.body)

    store_id = data.get("store")
    store = get_object_or_404(Store, pk=store_id)

    product = Product.objects.create(
        store=store,
        name=data.get("name", ""),
        description=data.get("description", ""),
        price=data.get("price", 0),
        stock=data.get("stock", 0),
        available=data.get("available", True),
    )

    return JsonResponse({"message": "Product created", "id": product.id}, status=201)


@csrf_exempt
def api_product_delete(request, pk):
    """
    Delete a product through the basic JSON API.
    """
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required"}, status=405)

    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return JsonResponse({"message": "Product deleted"})
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)


@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_create_store(request):
    """
    Create a store through the DRF API for the authenticated vendor.
    """
    data = request.data.copy()
    vendor_id = data.get("vendor")

    if vendor_id is None:
        return Response({"error": "Vendor field is required."}, status=status.HTTP_400_BAD_REQUEST)

    if int(vendor_id) != request.user.id:
        return Response(
            {"error": "You can only create a store for yourself."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = StoreSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_add_product(request):
    """
    Add a product through the DRF API to a store owned by the authenticated vendor.
    """
    data = request.data.copy()
    store_id = data.get("store")

    if store_id is None:
        return Response({"error": "Store field is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return Response({"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND)

    if store.vendor != request.user:
        return Response(
            {"error": "You can only add products to your own store"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def api_vendor_stores(request, vendor_id):
    """
    Return all stores for a given vendor.
    """
    stores = Store.objects.filter(vendor_id=vendor_id)
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_store_products(request, store_id):
    """
    Return all products for a given store.
    """
    products = Product.objects.filter(store_id=store_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@authentication_classes([BasicAuthentication])
def api_product_reviews(request, product_id):
    """
    Return or create reviews for a given product through the DRF API.
    """
    if request.method == "GET":
        reviews = Review.objects.filter(product_id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    if not request.user or not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data.copy()
    data["user"] = request.user.id
    data["product"] = product_id

    serializer = ReviewSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def reddit_feed(request):
    """
    Display a small Reddit feed from the Python subreddit.
    """
    posts = []
    error = None

    try:
        posts = get_reddit_posts(subreddit="python", limit=5)
    except Exception as e:
        error = str(e)

    return render(
        request,
        "store/reddit_feed.html",
        {
            "posts": posts,
            "error": error,
        },
    )