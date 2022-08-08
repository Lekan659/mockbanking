"""The Custom Authentication Backend"""
from .models import AuthModel

class AuthBackend(object):
    def authenticate(self, request, email, password):
        #fetch data from login model
        try:
            user = AuthModel.manage.get(email=email)
            if user:
                if user.check_password(password):
                    return user
                else:
                    return None
            else:
                #User does not exist
                return None
        except Exception:
            return None
    
    def get_user(self, user_id):
        try:
            return AuthModel.manage.get(id=user_id)
        except AuthModel.DoesNotExist:
            return None
