"""
    This model defines all system option variables
"""
from django.db import models

#Option Model Manager
class OptionModelManager(models.Manager):
    def c_get(self, **Kwargs):
        try:
            option = super().get(**Kwargs)
            return option
        except Exception:
            return None

    def getOptionByName(self, name):
        """Get option by option name"""
        try:
            option = super().get(name=name)
            return option.value
        except Exception:
            return None
    
    def getAllOptions(self)->dict:
        options = super().all()
        option_dict = {}
        for option in options:
            option_dict[option.name] = option.value
        return option_dict

    def getNextAccountNumber(self):
        """Get Next Account number"""
        option = super().filter(name="account_pointer")
        account_number = option[0].value
        option.update(value=models.F("value")+1)
        return account_number

#Option Model
class OptionModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Option Id")
    name = models.CharField(max_length=255, verbose_name="Option Name")
    value = models.CharField(max_length=50, verbose_name="Option Value")

    manage = OptionModelManager()

    class Meta:
        db_table = "bip_option"
    
        def __str__(self):
            return self.name
            
    def __str__(self):
            return self.name