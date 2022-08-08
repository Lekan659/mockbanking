"""
    State model: Represents Nigeria state
"""
from django.db import models

#State Model Manager
class StateModelManager(models.Manager):
    def c_get(self, **Kwargs):
        try:
            state = super().get(**Kwargs)
            return state
        except Exception:
            return None


#State Model
class StateModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    nicname = models.CharField(max_length=50, unique=True)

    manager = StateModelManager()

    class Meta:
        db_table = "bip_state"
    
        def __str__(self):
            return self.name
            
    def __str__(self):
            return self.name