from django.db import models

# Create your models here.

class Save_PE_Ratio(models.Model):

    date_time = models.DateTimeField(auto_now=True)
    value = models.CharField(max_length=25)