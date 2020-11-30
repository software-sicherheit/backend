# from djongo import models
from django.db import models
#from django_mysql.models import JSONField
import jsonfield

class MinioMeta(models.Model):
    uuid = models.CharField(max_length=10, primary_key=True)
    passwordKey = jsonfield.JSONField()
    rsaOAEP = jsonfield.JSONField()
    rsaPSS = jsonfield.JSONField()
    dataNameKey = jsonfield.JSONField()

    objects = models.Manager()