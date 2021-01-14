from core.models import *
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender = customUser)
def create_account(sender, created, instance, **kwargs):
    if created:
        if instance.account_type == 1:
            Admin.objects.create(admin = instance)

        if instance.account_type == 2:
            Buyer.objects.create(admin = instance)

        if instance.account_type == 3:
            Seller.objects.create(admin = instance)


@receiver(post_save, sender = customUser)
def save_account(sender, instance, **kwargs):
    if instance.account_type == 1:
        instance.admin.save()

    if instance.account_type == 2:
        instance.buyer.save()

    if instance.account_type == 3:
        instance.seller.save()