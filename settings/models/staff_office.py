"""
    This model defines the office for staff
    This is neccessary as staff can have more than one location. It is Location based permission
"""
from django.db import models
from .office_branch import OfficeBranchModel
from staff.models import StaffModel

#Staff Office Model Manager
class StaffOfficeModelManager(models.Manager):
    def c_get(self, **Kwargs):
        try:
            state = super().get(**Kwargs)
            return state
        except Exception:
            return None

#Staff Office Model
class StaffOfficeModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE, verbose_name="Staff Id", related_name="staff_office_model")
    office = models.ForeignKey(OfficeBranchModel, on_delete=models.CASCADE, verbose_name="Office Location Id", related_name="staff_office_model")
    date_asigned = models.DateTimeField(auto_now=True, verbose_name="Date Asigned")

    manage = StaffOfficeModelManager()

    class Meta:
        db_table = "bip_staff_office"
    
        def __str__(self):
            return self.id
            
    def __str__(self):
            return self.id