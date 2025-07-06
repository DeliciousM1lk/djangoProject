import logging
from django.dispatch import Signal, receiver
from .models import Film

logger = logging.getLogger("app.signals")

drama_film_created = Signal()

@receiver(drama_film_created, sender=Film, dispatch_uid="drama_film_signal_handler")
def handle_drama_film(sender, instance, **kwargs):
    logger.info(f"[DRAMA FILM] Фильм-драма создан: {instance.name} (год: {instance.year})")
