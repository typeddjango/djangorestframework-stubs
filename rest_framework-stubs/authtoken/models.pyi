from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Token(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="auth_token", on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    def generate_key(self) -> str: ...
