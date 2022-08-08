from rest_framework.exceptions import (
    APIException,
    NotFound,
    PermissionDenied,
    NotAuthenticated,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND
)


class TokenExpired(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_detail = "Access token expired"
    default_code = "token_expired"

class AuthenticationFailed(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_detail = "Authentication failed"
    default_code = "authentication_failed"