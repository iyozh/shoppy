from django.db.models.signals import post_save
from django.dispatch import receiver
from project.tasks import reindex_product
from applications.showcase.models import Product


@receiver(post_save, sender=Product)
def reindex_product_post_save(sender, instance, **kwargs):
    pass