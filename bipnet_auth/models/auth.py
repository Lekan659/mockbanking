""" Auth model """

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.db import models

IS_ACTIVE_OPTIONS = [False, True]

#Model Manager for AuthModel
class AuthModelManager(BaseUserManager):
    
    def is_valid_new_auth(self,email):
        try:
            user = super().get(email=email)
            return False
        except self.model.DoesNotExist:
            return True

    def create_auth(self,email,password,is_staff=False):
        try:
            user = super().get(email=email)
            return None
        except self.model.DoesNotExist:
            #add new user to database
            user = self.model(email=email,is_staff=is_staff,password=password)
            # user.set_password(password)
            user.save()
            return user

    def create_superuser(self,email,password,is_staff=True):
        
        try:
            user = super().get(email=email)
            return None
        except self.model.DoesNotExist:
            #add new user to database
            user = self.model(email=email,is_staff=is_staff,password=password)
            #old user.set_password(password)
            user.save()
            return user
    
    def c_get(self,**kwargs):
        try:
            user = super().get(**kwargs)
            return user
        except self.model.DoesNotExist:
            return None

#Auth Model
class AuthModel(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    password = models.CharField(max_length=128,verbose_name="Password")
    is_staff = models.BooleanField(default=True, verbose_name="Is Staff")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    last_login = models.DateTimeField(auto_now=True, verbose_name="Last Login")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    
    manage = AuthModelManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        db_table = "bip_auth"
    
        def __str__(self):
            return self.email
            
    def __str__(self):
            return self.email