"""
    This model defines the Branches of the office using the state
"""
from django.db import models
from .state import StateModel

#OfficeBranchModelManager
class OfficeBranchModelManager(models.Manager):
    def c_get(self, **Kwargs):
        try:
            state = super().get(**Kwargs)
            return state
        except Exception:
            return None

#OfficeBranchModel
class OfficeBranchModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Office Branch Id")
    state = models.ForeignKey(StateModel, on_delete=models.CASCADE, verbose_name="State Id")
    name = models.CharField(max_length=255, verbose_name="Office Branch Name")
    office_type = models.CharField(max_length=50, verbose_name="Office Type")

    manage = OfficeBranchModelManager()

    class Meta:
        db_table = "bip_office"
    
        def __str__(self):
            return self.name
            
    def __str__(self):
            return self.name