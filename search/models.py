from django.db import models

# Create your models here.
class SearchConfig(models.Model):   # To control search behaviour
    config_name= models.CharField(max_length= 128, db_index= True)
    config_value= models.CharField(max_length= 1024)

    def __str__(self):
        return "{:<16} {:<64}".format(self.config_name, self.config_value)