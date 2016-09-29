from django.db.models.signals import post_save
from django.dispatch import receiver

from act.models import Address


@receiver(post_save, sender=Address)
def set_default(instance, sender, created, **kwargs):
    if created:
        all_addresses = sender.objects.filter(user=instance.user)
        for address in all_addresses:
            address.default = False
            address.save()
        instance.default = True
        instance.save()
