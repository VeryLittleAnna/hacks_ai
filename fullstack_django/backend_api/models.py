from django.db import models


# Модуль работы с БД.
class NLPmodel(models.Model):
    address = models.CharField(max_length=100)
