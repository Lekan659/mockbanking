from rest_framework.authentication import BaseAuthentication, get_authorization_header
from .models import AuthTokenModel
from django.utils.translation import gettext_lazy as _
from .exceptions import TokenExpired, AuthenticationFailed
from datetime import datetime,timedelta
from bipnet.settings import EXPIRING_TOKEN_DURATION
from django.utils import timezone

class TokenAuthentication(BaseAuthentication):
    """
    Custom token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Token'
    model = AuthTokenModel

    """
    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.model
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid authentication token.'))

        if timezone.now() > token.expires:
            #Delete token before raising Token Expired exception
            
            token.delete()
            token = model.objects.select_related('user').get(key=key)
            raise TokenExpired(_('Token has expired'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        #Token is valid, renew token expiration time
        token.expires = timezone.now() + EXPIRING_TOKEN_DURATION
        token.save()

        return (token.user, token)
