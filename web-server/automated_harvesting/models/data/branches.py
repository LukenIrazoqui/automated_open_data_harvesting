from django.db import models


class Branches(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'branches'