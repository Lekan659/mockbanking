import binascii
import os

from django.conf import settings
from bipnet.settings import EXPIRING_TOKEN_DURATION
from django.db import models
from django.utils.translation import gettext_lazy as _
from .auth import AuthModel
from datetime import timedelta, datetime
from django.utils import timezone


class AuthTokenModel(models.Model):
    """
    The Custom authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        AuthModel, related_name='bip_auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    expires = models.DateTimeField(_("Expires"), blank=True, null=True)


    class Meta:
        db_table = "bip_auth_token"
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        
        if not self.key:
            self.key = self.generate_key()
        self.clean()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()
    
    
    def clean(self):
        if not self.expires:
            
            # (or do something with `self.period`?)
            self.expires = datetime.now() + EXPIRING_TOKEN_DURATION

    def __str__(self):
        return self.key
