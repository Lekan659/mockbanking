"""Staff Model"""

from django.db import models
from bipnet_auth.models import AuthModel

#Staff Model Declration
class StaffModel(models.Model):

    id = models.AutoField(primary_key=True)
    auth = models.OneToOneField(AuthModel, verbose_name='Authenticator', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    gender = models.CharField(max_length=6, verbose_name="Gender")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    position = models.CharField(max_length=50, verbose_name="position")
    avatar = models.ImageField(upload_to='media/avatars/staff/', null=True, blank=True, verbose_name="Avatar")

    class Meta:
        db_table = "bip_staff"
    
        def __str__(self):
            return self.id
            
    def __str__(self):
            return self.id