from django.db import models


class Bvbv(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'bvbv'