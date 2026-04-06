from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from store.models import Store, Product, Review, Order


class Command(BaseCommand):
    help = 'Create Buyers and Vendors groups with the correct permissions'

    def handle(self, *args, **kwargs):
        buyers_group, _ = Group.objects.get_or_create(name='Buyers')
        vendors_group, _ = Group.objects.get_or_create(name='Vendors')

        # Clear old permissions first
        buyers_group.permissions.clear()
        vendors_group.permissions.clear()

        # Content types
        store_ct = ContentType.objects.get_for_model(Store)
        product_ct = ContentType.objects.get_for_model(Product)
        review_ct = ContentType.objects.get_for_model(Review)
        order_ct = ContentType.objects.get_for_model(Order)

        # Vendor permissions
        vendor_permissions = Permission.objects.filter(
            content_type__in=[store_ct, product_ct],
            codename__in=[
                'add_store', 'view_store', 'change_store', 'delete_store',
                'add_product', 'view_product', 'change_product', 'delete_product',
            ]
        )

        # Buyer permissions
        buyer_permissions = Permission.objects.filter(
            content_type__in=[product_ct, review_ct, order_ct],
            codename__in=[
                'view_product',
                'add_review', 'view_review',
                'add_order', 'view_order',
            ]
        )

        vendors_group.permissions.set(vendor_permissions)
        buyers_group.permissions.set(buyer_permissions)

        self.stdout.write(self.style.SUCCESS('Buyers and Vendors groups created successfully.'))