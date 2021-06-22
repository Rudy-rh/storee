from django.apps import AppConfig
from django.db.models.signals import post_save


class BarberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.barber'
    label = 'barber'

    def ready(self):
        Brochure = self.get_model('Brochure')

        from .signals import brochure_save_handler

        # post_save.connect(brochure_save_handler, sender=Brochure,
        #                   dispatch_uid='brochure_signal')
