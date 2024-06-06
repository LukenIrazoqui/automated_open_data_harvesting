from django.db import models


class Precision(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'precision'
        verbose_name = "Précisions"
    
    def __str__(self):
        return self.name 