from django.db import transaction


@transaction.atomic()
def brochure_save_handler(sender, instance, created, **kwargs):
    if instance.is_active == True:
        cls = instance.__class__
        instnaces = cls.objects \
            .filter(is_active=True) \
            .exclude(uuid=instance.uuid)

        if instnaces.exists():
            instnaces.update(is_active=False)
