"""
    This model defines the Permissions for staff
"""
from django.db import models

PERMISSION_CATEGORIES = (
    ('basic','Basic'),
    ('management','Management'),
    ('admin','Admin'),
    ('teller','Teller')
)
#PermissionModelManager
class PermissionModelManager(models.Manager):
    def c_get(self, **Kwargs):
        try:
            state = super().get(**Kwargs)
            return state
        except Exception:
            return None

#Permission Model
class PermissionModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Permission Id")
    display_name = models.CharField(max_length=255, default="Permission Name", verbose_name="Permission Display Name")
    name = models.CharField(max_length=255, verbose_name="Permission Name")
    category = models.CharField(max_length=25, choices=PERMISSION_CATEGORIES, verbose_name="Category")

    manage = PermissionModelManager()

    class Meta:
        db_table = "bip_permission"
    
        def __str__(self):
            return self.name
            
    def __str__(self):
            return self.name