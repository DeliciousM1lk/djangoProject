# signals
import logging
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone

logger = logging.getLogger(__name__)


def log_user_login(sender, request, user, **kwargs):
    logger.info(f"User {user_logged_in} logged in. Username: {user.username}. Time: {timezone.now()}")


user_logged_in.connect(
    log_user_login,
    dispatch_uid="user_logged_in_signal")
