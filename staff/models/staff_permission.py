"""
    This model defines the Permissions for staff
"""
from django.db import models
from .permission import PermissionModel
from .staff import StaffModel

#Staff Permission Model Manager
class StaffPermissionModelManager(models.Manager):
    def c_get(self, **Kwargs):
        try:
            state = super().get(**Kwargs)
            return state
        except Exception:
            return None

#Staff Permission Model
class StaffPermissionModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE, verbose_name="Staff Id", related_name="staff_id")
    permission = models.ForeignKey(PermissionModel, on_delete=models.CASCADE, verbose_name="Permission Id")
    date_asigned = models.DateTimeField(auto_now=True, verbose_name="Date Asigned")

    manage = StaffPermissionModelManager()

    class Meta:
        db_table = "bip_staff_permission"
    
        def __str__(self):
            return self.id
            
    def __str__(self):
            return self.id